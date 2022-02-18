import requests
import django
import os
import time
import datetime
from pprint import pprint

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.settings'
django.setup()
from stremstv.models import League, Event


SPORTS_IDS = (1, 2, 3, 4, 6, 9, 19, 26, 56, 189)
TABLE_MARKETS_IDS = {
    1: {
        'Название': 'Исход',
        1: 'П1',
        2: 'X',
        3: 'П2'
    },
    8: {
        'Название': 'Двойной шанс',
        4: 'X1',
        5: '12',
        6: 'X2',
    },
    17: {
        'Название': 'Тотал',
        9: 'Больше',
        10: 'Меньше'
    },
    2: {
        'Название': 'Фора',
        7: 'Фора 1',
        8: 'Фора 2'
    },
    15: {
        'Название': 'Тотал ком.1',
        12: 'Меньше',
        11: 'Больше'
    },
    62: {
        'Название': 'Тотал ком.2',
        13: 'Больше',
        14: 'Меньше'
    }
}


def check_leagues():
    with requests.session() as session:
        while True:
            for sport_id in SPORTS_IDS:
                api = f'https://1xstavka.ru/LineFeed/GetChampsZip?sport={sport_id}&tf=2200000&tz=3&country=1&partner=51&virtualSports=true'
                response = session.get(api).json()
                if response['Success']:
                    for l in response['Value']:
                        league_name = l['L']
                        league_id = l['LI']
                        sport_name = l['SN']
                        league = None
                        if League.objects.filter(league=league_name, sport=sport_name, include=False).exists():
                            continue
                        else:
                            api2 = f'https://1xstavka.ru/LineFeed/Get1x2_VZip?sports={sport_id}&champs={league_id}&count=500&tf=2200000&tz=3&antisports=188&mode=4&country=1&partner=51&getEmpty=true'
                            response2 = session.get(api2).json()
                            if response2['Success']:
                                for i in response2['Value']:
                                    if not league:
                                        country = i['CN']
                                        league = League.objects.get_or_create(league=league_name, sport=sport_name, country=country)[0]
                                        continue
                                    elif not league.include:
                                        continue
                                    home = i.get('O1')
                                    away = i.get('O2')
                                    if sport_name in ['Биатлон', 'Формула 1']:
                                        if 'Биатлон' in sport_name:
                                            logo = 'https://w7.pngwing.com/pngs/513/262/png-transparent-skiing-ski-superhero-sports-equipment-fictional-character.png'
                                        else:
                                            logo = 'https://w7.pngwing.com/pngs/749/255/png-transparent-formula-1-logo-abu-dhabi-grand-prix-2018-fia-formula-one-world-championship-european-grand-prix-logo-auto-racing-formula-1-miscellaneous-text-trademark.png'
                                        home, away = sport_name, sport_name
                                        home_logo, away_logo = logo, logo
                                    elif not home and not away:
                                        continue
                                    else:
                                        home_logo = 'https://cdn.1xstavka.ru/sfiles/logo_teams/' + i['O1IMG'][0] if i['O1IMG'] else None
                                        away_logo = 'https://cdn.1xstavka.ru/sfiles/logo_teams/' + i['O2IMG'][0] if i['O2IMG'] else None
                                    status = 'prematch'
                                    start = datetime.datetime.fromtimestamp(i['S'])
                                    markets = {}
                                    for m in i['E']:
                                        if m['G'] not in TABLE_MARKETS_IDS:
                                            continue
                                        m2 = TABLE_MARKETS_IDS[m['G']]
                                        if m2['Название'] not in markets:
                                            markets[m2['Название']] = {}
                                        if 'P' in m:
                                            if m['P'] not in markets[m2['Название']]:
                                                markets[m2['Название']][str(m['P'])] = {m2[m['T']]: m['C']}
                                            else:
                                                markets[m2['Название']][str(m['P'])][m2['T']] = m['C']
                                        else:
                                            markets[m2['Название']][m2[m['T']]] = m['C']
                                    if 'MIO' in i:
                                        stage = i['MIO'].get('TSt')
                                    else:
                                        stage = None
                                    if Event.objects.filter(sport=sport_name, country=country, league=league_name, home=home, away=away, start__date=start.date()).exists():
                                        event = Event.objects.get(sport=sport_name, country=country, league=league_name, home=home, away=away, start__date=start.date())
                                        event.start = start
                                        event.status = status
                                        event.markets = markets
                                        event.save()
                                    else:
                                        Event.objects.create(
                                            xbet_id=i['I'],
                                            sport=sport_name,
                                            country=country,
                                            league=league_name,
                                            stage=stage,
                                            home=home,
                                            away=away,
                                            home_logo=home_logo,
                                            away_logo=away_logo,
                                            status=status,
                                            start=start,
                                            markets=markets,
                                            include=False if league.exclude else True
                                        )

            time.sleep(60)


if __name__ == '__main__':
    while True:
        try:
            check_leagues()
        except requests.exceptions.ConnectionError:
            continue
