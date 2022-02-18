import ujson
import random
from stremstv.models import Event, League, News


def reviews(sport, cache):
    if sport == '0':
        events = Event.objects.filter(status='complete', sport='Футбол', include=True).order_by('status', 'start')
    elif sport == '1':
        events = Event.objects.filter(status='complete', sport='Хоккей', include=True).order_by('status', 'start')
    elif sport == '2':
        events = Event.objects.filter(status='complete', sport='Биатлон', include=True).order_by('status', 'start')
    elif sport == '3':
        events = Event.objects.filter(status='complete', sport__in=['Бокс', 'UFC', 'Единоборства'], include=True).order_by('status', 'start')
    else:
        events = Event.objects.filter(status='complete', sport__in=['Баскетбол', 'Формула 1', 'Волейбол', 'Теннис'], include=True).order_by('status', 'start')

    context = {'events': []}
    for event in events:
        league = cache.get(f'{event.sport}-{event.league}')
        if not league:
            league = League.objects.get(sport=event.sport, league=event.league, include=True)
            cache.set(f'{event.sport}-{event.league}', league, timeout=600)
        day = event.start.day
        month = event.start.month
        month = month if month > 9 else f'0{month}'
        day = day if day > 9 else f'0{day}'
        status = f'{day}.{month}'
        context['events'].append({
            'id': event.id,
            'league': league.title if league.title else event.league,
            'home': event.home if not event.title else event.title.split(' - ')[0],
            'away': event.away if not event.title else event.title.split(' - ')[1],
            'score': f'{event.score_home}-{event.score_away}',
            'status': status,
            'home_logo': event.home_logo,
            'away_logo': event.away_logo,
            'stream': event.stream
        })
    return ujson.dumps(context).encode()


def event_list(sport, cache):
    if sport == '0':
        events = Event.objects.filter(status__in=['live', 'prematch'], sport='Футбол', include=True).order_by('status', 'start')
    elif sport == '1':
        events = Event.objects.filter(status__in=['live', 'prematch'], sport='Хоккей', include=True).order_by('status', 'start')
    elif sport == '2':
        events = Event.objects.filter(status__in=['live', 'prematch'], sport='Биатлон', include=True).order_by('status', 'start')
    elif sport == '3':
        events = Event.objects.filter(status__in=['live', 'prematch'], sport__in=['Бокс', 'UFC', 'Единоборства'], include=True).order_by('status', 'start')
    else:
        events = Event.objects.filter(status__in=['live', 'prematch'], sport__in=['Баскетбол', 'Формула 1', 'Волейбол', 'Теннис'], include=True).order_by('status', 'start')

    COLORS = {
        'Жёлтый': '#f3c300',
        'Красный': '#f73434',
        'Синий': '#38a5db',
        'Random': ['#f3c300', '#f73434', '#38a5db']
    }

    context = {'events': []}
    for event in events:
        score_periods = ''
        league = cache.get(f'{event.sport}-{event.league}')
        if not league:
            league = League.objects.get(sport=event.sport, league=event.league, include=True)
            cache.set(f'{event.sport}-{event.league}', league, timeout=600)
        if event.status == 'live':
            if event.time_seconds:
                minute = int(event.time_seconds / 60)
            else:
                minute = None
            status = event.live_status
            score = f'{event.score_home}-{event.score_away}'
            if event.score_periods:
                periods = eval(event.score_periods)
                for p in periods:
                    score_periods += f'{p[0]}:{p[1]}, '
                    score_periods = score_periods[:-2]
        else:
            minute = None
            day = event.start.day
            month = event.start.month
            hour = event.start.hour
            minu = event.start.minute
            month = month if month > 9 else f'0{month}'
            day = day if day > 9 else f'0{day}'
            hour = hour if hour > 9 else f'0{hour}'
            minu = minu if minu > 9 else f'0{minu}'
            status = f'{day}.{month}'
            score = f'{hour}:{minu}'
        context['events'].append({
            'id': event.id,
            'league': event.league if not league.title else league.title,
            'home': event.home if not event.title else event.title.split(' - ')[0],
            'away': event.away if not event.title else event.title.split(' - ')[1],
            'minute': minute,
            'score': score,
            'periods': score_periods,
            'status': status,
            'color': COLORS[event.color] if event.color != 'Random' else random.choice(COLORS['Random']),
            'home_logo': event.home_logo,
            'away_logo': event.away_logo,
            'stream': event.stream
        })
    return ujson.dumps(context).encode()
