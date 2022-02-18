import datetime
import ujson
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q, Sum
from django.contrib.auth import authenticate, login, logout
from referral.models import Referral, ReferralUser, ModalPage
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import caches


def referral_auth(request):
    if request.method == 'GET':
        return render(request, 'auth.html', {'log': 'false'})
    elif request.POST:
        if request.POST['auth_type'] == 'register':
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            phone = request.POST['phone']
            site = request.POST['site']
            if Referral.objects.filter(username=username).exists():
                return render(request, 'auth.html', {'error': 'Nickname занят!', 'log': 'true'})
            if Referral.objects.filter(email=email).exists():
                return render(request, 'auth.html', {'error': 'Email занят!', 'log': 'true'})
            Referral.objects.create_user(
                username=username, password=password, email=email, phone=phone, site=site
            )
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/referral/')

        elif request.POST['auth_type'] == 'login':
            q = Q(username=request.POST['username']) | Q(email=request.POST['username'])
            ref_user = Referral.objects.filter(q)
            if ref_user.exists():
                username = ref_user.first().username
                user = authenticate(request, username=username, password=request.POST['password'])
                if not user:
                    return render(request, 'auth.html', {'error': 'Неверный пароль!', 'log': 'false'})
                login(request, user)
                return HttpResponseRedirect('/referral/')
            else:
                return render(request, 'auth.html', {'error': 'Пользователь не найден!', 'log': 'false'})
            pass


def referral(request):
    if request.user.is_authenticated:
        cache = caches['query']
        cache.add('modals', ModalPage.objects.order_by('position'), timeout=60)
        modals = cache.get('modals')
        if not request.user.is_staff:
            ref = request.user.referral
            context = {
                'username': ref.username,
                'link': f'https://{request.build_absolute_uri().split("/")[2]}/landing/?token={ref.token}',
            }
            referrals = ReferralUser.objects.filter(ref_token=ref.token)
        else:
            context = {}
            referrals = ReferralUser.objects.all()

        stats = {
            'rows': [],
            'total': {
                'views': 0,
                'downloads': 0,
            }
        }
        now = datetime.datetime.now()
        start = now.date() - datetime.timedelta(days=10)
        end = now.date()
        referrals = referrals.filter(create__date__range=[start, end])
        context['start'] = start.isoformat()
        context['end'] = end.isoformat()
        dates = referrals.distinct('create__date').values('create__date')
        balance = referrals.aggregate(Sum('paid'))['paid__sum']
        for d in reversed(dates):
            date = d['create__date'].isoformat()
            views = referrals.filter(create__date=date).count()
            downloads = referrals.filter(create__date=date, download=True).count()
            stats['rows'].append({
                'date': date,
                'views': views,
                'downloads': downloads
            })
            stats['total']['views'] += views
            stats['total']['downloads'] += downloads
        context['rows'] = stats['rows']
        context['total'] = stats['total']
        context['balance'] = balance
        context['modals'] = modals
        return render(request, 'referral.html', context)
    else:
        return HttpResponseRedirect('/referral/auth/')


@csrf_exempt
def referral_filter(request):
    if request.method == 'POST' and request.user.is_authenticated:
        js = ujson.loads(request.body)
        referrals = ReferralUser.objects.filter(create__date__range=[js['start'], js['end']])
        if js.get('ntk') == 'nick':
            token = Referral.objects.get(username=js.get('nt')).token
        else:
            token = js.get('nt')
        if token:
            referrals = referrals.filter(token=token)
        dates = referrals.distinct('create__date').values('create__date')
        balance = referrals.aggregate(Sum('paid'))['paid__sum']
        stats = {
            'rows': [],
            'total': {
                'views': 0,
                'downloads': 0,
            }
        }
        for d in reversed(dates):
            date = d['create__date'].isoformat()
            views = referrals.filter(create__date=date).count()
            downloads = referrals.filter(create__date=date, download=True).count()
            stats['rows'].append({
                'date': date,
                'views': views,
                'downloads': downloads
            })
            stats['total']['views'] += views
            stats['total']['downloads'] += downloads

        context = {
            'rows': stats['rows'],
            'total': stats['total'],
            'balance': balance
        }
        return JsonResponse(context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/referral/auth/')