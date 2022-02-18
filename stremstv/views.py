import json
import random
import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib.sessions.models import Session
from stremstv.models import Event, League, News
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import caches
from asgiref.sync import sync_to_async
from stremstv import query_caches


@csrf_exempt
def index(request):
    print('+')
    if not request.user.is_authenticated:
        request.session.set_expiry(60)
    cache = caches['template']
    cache.add('index', render(request, 'index.html'))
    return cache.get('index')


@csrf_exempt
def index2(request):
    if not request.user.is_authenticated:
        request.session.set_expiry(60)
    cache = caches['template']
    cache.add('index2', render(request, 'index2.html'))
    return cache.get('index2')


@csrf_exempt
def review(request):
    if not request.user.is_authenticated:
        request.session.set_expiry(60)
    cache = caches['template']
    cache.add('obzor', render(request, 'obzor.html'))
    return cache.get('obzor')


@csrf_exempt
def news_view(request):
    if request.POST:
        if not request.user.is_authenticated:
            request.session.set_expiry(60)
        news = News.objects.get(id=int(request.POST['id']))
        news.views += 1
        news.save()
        return JsonResponse({'success': True})


@csrf_exempt
def story(request):
    if not request.user.is_authenticated:
        request.session.set_expiry(60)
    cache = caches['query']
    cache.add('story', News.objects.filter(hidden=False), timeout=300)
    context = {'news': cache.get('story')}
    cache_temp = caches['template']
    cache_temp.add('story', render(request, 'story.html', context), timeout=300)
    return cache_temp.get('story')


@csrf_exempt
def story2(request):
    if not request.user.is_authenticated:
        request.session.set_expiry(60)
    context = {'news': News.objects.filter(hidden=False)}
    return render(request, 'story2.html', context)


@csrf_exempt
def get_reviews(request):
    if not request.user.is_authenticated:
        request.session.set_expiry(60)

    if request.POST:
        cache_keys = {
            '0': 'r0',
            '1': 'r1',
            '2': 'r2',
            '3': 'r3',
            '4': 'r4'
        }
        key = cache_keys[request.POST['p']]
        cache = caches['template'].get(key)
        if not cache:
            cache = query_caches.reviews(request.POST['p'], caches['query'])
            caches['template'].set(key, cache, timeout=60)
        return HttpResponse(cache, content_type='application/json')


@csrf_exempt
def get_events(request):
    if not request.user.is_authenticated:
        request.session.set_expiry(60)

    if request.POST:
        cache_keys = {
            '0': '0',
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4'
        }
        key = cache_keys[request.POST['p']]
        print(key)
        cache = caches['template'].get(key)
        if not cache:
            cache = query_caches.event_list(request.POST['p'], caches['query'])
            caches['template'].set(key, cache, timeout=15)
        return HttpResponse(cache, content_type='application/json')


@csrf_exempt
def event_page(request, event_id):
    if not request.user.is_authenticated:
        request.session.set_expiry(60)
    cache = caches['query']
    cache.add(f'{event_id}', Event.objects.get(id=event_id), timeout=20)
    event = cache.get(f'{event_id}')
    if event.stream:
        stream = event.stream
    else:
        stream = f'/player/{event_id}/'
    if event.status in ('live', 'complete'):
        score = f'{event.score_home}-{event.score_away}'
    else:
        score = ''

    score_periods = ''
    if event.score_periods:
        periods = eval(event.score_periods)
        if len(periods) > 1:
            for p in periods:
                score_periods += f'{p[0]}:{p[1]}, '
    if score_periods:
        score_periods = f'({score_periods[:-2]})'

    cache_temp = caches['template']
    cache_temp.add(
        'chat2',
        render(request, 'chat2.html', {
            'event_id': event.id,
            'stream': stream,
            'home': event.home,
            'away': event.away,
            'home_logo': event.home_logo,
            'away_logo': event.away_logo,
            'title': f'{event.home} - {event.away}',
            'score': score,
            "periods": score_periods,
            'status': event.live_status if event.live_status else '',
            'time': f"{int(event.time_seconds / 60)}'" if event.time_seconds else ''
        }),
        timeout=30
    )


@csrf_exempt
def check_event(request):
    if not request.user.is_authenticated:
        request.session.set_expiry(60)
    if request.POST:
        event_id = int(request.POST['i'])
        cache = caches['query']
        cache.add(f'{event_id}', Event.objects.get(id=event_id), timeout=20)
        event = cache.get(f'{event_id}')
        if event.status in ('live', 'complete'):
            score = f'{event.score_home}-{event.score_away}'
        else:
            score = ''
        score_periods = ''
        if event.score_periods:
            periods = eval(score_periods)
            if len(periods) > 1:
                for p in periods:
                    score_periods += f'{p[0]}:{p[1]}, '
        if score_periods:
            score_periods = f'({score_periods[:-2]})'
        title = f'{event.home} - {event.away}'
        context = {
            'title': title,
            'score': score,
            'periods': score_periods,
            'status': event.live_status if event.live_status else '',
            'time': f"{int(event.time_seconds / 60)}'" if event.time_seconds > 0 else ''
        }
        return JsonResponse(context)


@csrf_exempt
def player(request, event_id):
    if not request.user.is_authenticated:
        request.session.set_expiry(60)
    cache = caches['query']
    cache.add(f'{event_id}', Event.objects.get(id=event_id), timeout=20)
    event = cache.get(f'{event_id}')
    cache_temp = caches['template']
    cache_temp.add(f'pl{event_id}', render(request, 'player.html', {'stream': event.stream}), timeout=30)
    return cache_temp.get(f'pl{event_id}')


@csrf_exempt
def check_session(request):
    if not request.user.is_authenticated:
        request.session.set_expiry(60)
    return JsonResponse({'success': True})


@csrf_exempt
def check_online(request):
    if request.user.is_staff and request.POST:
        old_time = datetime.datetime.now() - datetime.timedelta(minutes=10)
        Session.objects.filter(expire_date__lt=old_time).delete()
        online = Session.objects.filter(expire_date__gt=datetime.datetime.now()).count()
        return JsonResponse({'online': online})
