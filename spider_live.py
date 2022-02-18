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
        api = 'https://1xstavka.ru/LiveFeed/Get1x2_VZip?sports=1,2,3,4,6,9,19,26,56,189&count=5000&antisports=188&mode=4&country=1&partner=51&getEmpty=true&noFilterBlockEvent=true'
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
                status = 'live'
                start = datetime.datetime.fromtimestamp(i['S'])
                score_home = None
                score_away = None
                score_periods = []
                stats = []
                if 'SC' in i:
                    live_status = i['SC'].get('CPS')
                    if not live_status:
                        continue
                    if 'Игра завершена' in live_status:
                        status = 'complete'
                    time_seconds = i['SC'].get('TS')
                    if not time_seconds:
                        time_seconds = 0
                    score_home = i['SC']['FS']['S1'] if 'S1' in i['SC']['FS'] else 0
                    score_away = i['SC']['FS']['S2'] if 'S2' in i['SC']['FS'] else 0
                    if 'PS' in i['SC']:
                        for p in i['SC']['PS']:
                            if 'Value' in p:
                                s1 = p['Value']['S1'] if 'S1' in p['Value'] else 0
                                s2 = p['Value']['S2'] if 'S2' in p['Value'] else 0
                                score_periods.append([s1, s2])
                    if 'ST' in i['SC']:
                        for s in i['SC']['ST']:
                            for v in s['Value']:
                                if v['ID'] in STATISTICS_ID['Футбол']:
                                    stats.append({
                                        'id': v['ID'],
                                        'key': STATISTICS_ID['Футбол'][v['ID']],
                                        'values': [v.get('S1'), v.get('S2')]
                                    })
                else:
                    live_status = None
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
                score_periods = str(score_periods)
                if 'MIO' in i:
                    stage = i['MIO'].get('TSt')
                else:
                    stage = None
                if Event.objects.filter(sport=sport, country=country, league=league, home=home, away=away, start__date=start.date()).exists():
                    event = Event.objects.get(sport=sport, country=country, league=league, home=home, away=away, start__date=start.date())
                    event.xbet_id = i['I']
                    event.score_home = score_home
                    event.score_away = score_away
                    event.time_seconds = time_seconds
                    event.score_periods = score_periods
                    event.status = status
                    event.stats = stats
                    event.live_status = live_status
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
                        score_home=score_home,
                        score_away=score_away,
                        score_periods=score_periods,
                        status=status,
                        start=start,
                        live_status=live_status,
                        markets=markets,
                        stats=stats,
                        time_seconds=time_seconds,
                        include=include,
                    )
            time.sleep(1)


if __name__ == '__main__':
    while True:
        try:
            scan_xbet()
        except requests.exceptions.ConnectionError:
            continue
