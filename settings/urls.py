from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from landing.views import landing, load_apk
from referral.views import referral_auth, referral, logout_view, referral_filter
from stremstv.views import (
    index, get_events, player, review, get_reviews, event_page, index2, check_event, check_session, check_online,
    story, news_view
)

urlpatterns = [
    # pages
    path('admin/', admin.site.urls),
    path('main/', index2),
    path('obzor/', review),
    path('story/', story),
    path('landing/', landing),
    path('logout/', logout_view),
    path('referral/', referral),
    path('referral/auth/', referral_auth),
    path('event/<int:event_id>/', event_page),
    path('player/<int:event_id>/', player),
    path('tinymce/', include('tinymce.urls')),

    # endpoints
    path('api/get_reviews/', get_reviews),
    path('api/get_events/', get_events),
    path('api/check_event/', check_event),
    path('api/check_session/', check_session),
    path('api/check_online/', check_online),
    path('api/news_view/', news_view),
    path('api/load_apk/', load_apk),
    path('api/ref_filter/', referral_filter),

    path('', index)
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
