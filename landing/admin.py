from django.contrib import admin
from .models import APK


@admin.register(APK)
class APKAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'downloads')
    list_display_links = ('__str__', 'downloads')