from django.contrib import admin
from .models import Event, League, News


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_filter = ('sport', 'include', 'country')
    list_display = ('sport', 'country', 'league', 'include')
    list_display_links = ('sport', 'country', 'league')
    list_editable = ['include']
    search_fields = ['league']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_filter = ('sport', 'status', 'include', 'country')
    list_display = ('start', 'sport', 'league', 'home', 'away', 'status', 'include')
    list_display_links = ('start', 'sport', 'league', 'home', 'away', 'status')
    list_editable = ['include']
    date_hierarchy = 'start'
    search_fields = ('home', 'away', 'league')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'views')

