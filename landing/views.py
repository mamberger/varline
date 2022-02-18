import json
import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from .models import APK
from referral.models import Referral, ReferralUser
from django.core.cache import caches


def landing(request):
    cache = caches['query']
    cache.add('apk', APK.objects.first(), timeout=400)
    apk = cache.get('apk')
    url = f'/media/'+str(apk.apk_file)
    if request.GET:
        token = request.GET.get('token')
        if token:
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
            else:
                ip = request.META['REMOTE_ADDR']
            user_agent = request.headers.get('User-Agent')
            if user_agent:
                if not ReferralUser.objects.filter(ref_token=token, ip_address=ip, user_agent=user_agent).exists():
                    ReferralUser.objects.create(
                        ref_token=token,
                        ip_address=ip,
                        user_agent=user_agent
                    )
    temp_cache = cache['template']
    temp_cache.add('langing', render(request, 'landing.html', {'apk': url}), timeout=500)
    return temp_cache.get('landing')


def load_apk(request):
    if request.method == 'POST':
        apk = APK.objects.first()
        apk.downloads += 1
        apk.save()
        js = json.loads(request.body)
        referer = js['referer']
        if 'token=' in referer:
            token = referer.split('token=')[-1]
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
            else:
                ip = request.META['REMOTE_ADDR']
            user_agent = request.headers.get('User-Agent')
            if user_agent:
                ref_user = ReferralUser.objects.filter(ref_token=token, ip_address=ip, user_agent=user_agent)
                if ref_user.exists():
                    ref_user = ref_user.first()
                    ref_user.download = True
                    ref_user.save()
        return JsonResponse({'success': True})
