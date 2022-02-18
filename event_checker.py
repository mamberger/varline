import datetime
import time
import requests
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.settings'
django.setup()
from stremstv.models import Event

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


def check():
    with requests.Session() as session:
        while True:
            events = Event.objects.filter(status='live')
            for event in events:
                api = f'https://1xstavka.ru/LiveFeed/GetGameZip?id={event.xbet_id}&lng=ru&cfview=0&isSubGames=true&GroupEvents=true&allEventsGroupSubGames=true&countevents=250&partner=51&grMode=2&marketType=1'
                if event.sport == 'Футбол':
                    if int(event.time_seconds/60) >= 85:
                        response = session.get(api).json()
                        if response['Success']:
                            i = response['Value']
                            if 'SC' in i:
                                status = i['SC'].get('CPS')
                                if status and 'Игра завершена' in status:
                                    event.status = 'complete'
                                event.score_home = i['SC']['FS']['S1'] if 'S1' in i['SC']['FS'] else 0
                                event.score_away = i['SC']['FS']['S2'] if 'S2' in i['SC']['FS'] else 0
                                stats = []
                                if 'ST' in i['SC']:
                                    for s in i['SC']['ST']:
                                        for v in s['Value']:
                                            if v['ID'] in STATISTICS_ID['Футбол']:
                                                stats.append({
                                                    'id': v['ID'],
                                                    'key': STATISTICS_ID['Футбол'][v['ID']],
                                                    'values': [v.get('S1'), v.get('S2')]
                                                })
                                score_periods = []
                                if 'PS' in i['SC']:
                                    for p in i['SC']['PS']:
                                        if 'Value' in p:
                                            s1 = p['Value']['S1'] if 'S1' in p['Value'] else 0
                                            s2 = p['Value']['S2'] if 'S2' in p['Value'] else 0
                                            score_periods.append([s1, s2])
                                event.stats = stats
                                event.score_periods = score_periods
                                event.save()
                        else:
                            event.status = 'complete'
                            event.save()
                elif event.sport in ('Теннис', 'Баскетбол', 'Волейбол', 'Хоккей'):
                    response = session.get(api).json()
                    if not response['Success']:
                        event.status = 'complete'
                        event.save()
                    else:
                        i = response['Value']
                        if 'SC' in i:
                            status = i['SC'].get('CPS')
                            if status and 'Игра завершена' in status:
                                event.status = 'complete'
                            event.score_home = i['SC']['FS']['S1'] if 'S1' in i['SC']['FS'] else 0
                            event.score_away = i['SC']['FS']['S2'] if 'S2' in i['SC']['FS'] else 0
                            score_periods = []
                            if 'PS' in i['SC']:
                                for p in i['SC']['PS']:
                                    if 'Value' in p:
                                        s1 = p['Value']['S1'] if 'S1' in p['Value'] else 0
                                        s2 = p['Value']['S2'] if 'S2' in p['Value'] else 0
                                        score_periods.append([s1, s2])
                            event.score_periods = score_periods
                            event.save()
            time.sleep(5)


if __name__ == '__main__':
    while True:
        try:
            check()
        except requests.exceptions.ConnectionError:
            continue
