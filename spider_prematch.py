import datetime
import time
import requests
import os
import django
from pprint import pprint

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.settings'
django.setup()
from stremstv.models import Event, League

STATISTICS_ID = {
    'Футбол': {
        45: 'Атаки',
        58: 'Опасные атаки',
        29: 'Владение мячом',
        59: 'Удары в створ',
        60: 'Удары в сторону ворот',
        70: 'Угловые',
        26: 'Жёлтые карточки',
        71: 'Красные карточки',
        72: 'Пенальти',
    },
    'Хоккей': {
        45: 'Атаки',
        17: 'Броски',
        18: 'Штрафы',
        20: 'Владение',
    },
}
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


def scan_xbet():
    with requests.Session() as session:
        api = 'https://1xstavka.ru/LineFeed/Get1x2_VZip?sports=1,2,3,4,6,9,19,26,56,189&count=5000&tf=2200000&tz=3&antisports=188&mode=4&country=1&partner=51&getEmpty=true'
        while True:
            response = session.get(api).json()
            for i in response['Value']:
                league = i['L']
                if 'x' in league:
                    continue
                elif 'CN' not in i:
                    continue
                country = i['CN']
                sport = i['SN']
                if League.objects.filter(sport=sport, country=country, league=league, include=False).exists():
                    continue
                elif not League.objects.filter(sport=sport, country=country, league=league).exists():
                    League.objects.create(sport=sport, country=country, league=league)
                    continue
                elif League.objects.filter(sport=sport, country=country, league=league, exclude=True).exists():
                    include = False
                else:
                    include = True
                home = i.get('O1')
                away = i.get('O2')
                if sport in ['Биатлон', 'Формула 1']:
                    if 'Биатлон' in sport:
                        logo = 'https://w7.pngwing.com/pngs/513/262/png-transparent-skiing-ski-superhero-sports-equipment-fictional-character.png'
                    else:
                        logo = 'https://w7.pngwing.com/pngs/749/255/png-transparent-formula-1-logo-abu-dhabi-grand-prix-2018-fia-formula-one-world-championship-european-grand-prix-logo-auto-racing-formula-1-miscellaneous-text-trademark.png'
                    home, away = sport, sport
                    home_logo, away_logo = logo, logo
                elif not home and not away:
                    continue
                else:
                    home_logo = 'https://cdn.1xstavka.ru/sfiles/logo_teams/' + i['O1IMG'][0] if i['O1IMG'] else None
                    away_logo = 'https://cdn.1xstavka.ru/sfiles/logo_teams/' + i['O2IMG'][0] if i['O2IMG'] else None
                status = 'prematch'
                start = datetime.datetime.fromtimestamp(i['S'])
                markets = {}
                if 'E' in i:
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
                if Event.objects.filter(sport=sport, country=country, league=league, home=home, away=away, start__date=start.date()).exists():
                    event = Event.objects.get(sport=sport, country=country, league=league, home=home, away=away, start__date=start.date())
                    event.start = start
                    event.status = status
                    event.markets = markets
                    event.save()
                else:
                    Event.objects.create(
                        xbet_id=i['I'],
                        sport=sport,
                        country=country,
                        league=league,
                        stage=stage,
                        home=home,
                        away=away,
                        home_logo=home_logo,
                        away_logo=away_logo,
                        status=status,
                        start=start,
                        markets=markets,
                        include=include,
                    )
            time.sleep(30)


if __name__ == '__main__':
    while True:
        try:
            scan_xbet()
        except requests.exceptions.ConnectionError:
            continue
