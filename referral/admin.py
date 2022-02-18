from django.contrib import admin
from .models import Referral, ReferralUser, ModalPage


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('username', 'token', 'balance')
    list_display_links = ('username', 'token', 'balance')


@admin.register(ReferralUser)
class ReferralUserAdmin(admin.ModelAdmin):
    list_display = ('ref_token', 'ip_address', 'user_agent', 'download', 'create')
    list_display_links = ('ref_token', 'ip_address', 'user_agent', 'download', 'create')
    search_fields = ('ref_token', 'ip_address', 'user_agent')


@admin.register(ModalPage)
class ModalPageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'position')
    list_editable = ['position']
