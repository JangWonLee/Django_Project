from django.contrib import admin
from mynews.models import News, Spot


class NewsAdmin(admin.ModelAdmin):
    fields = ['link_text', 'title_text', 'summary_text', 'opinion_text', 'pub_date']

    list_display = ('link_text', 'title_text', 'summary_text', 'opinion_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['title_text']

admin.site.register(News, NewsAdmin)

class SpotAdmin(admin.ModelAdmin):
    fields = ['henryhub_text', 'wticushing_text', 'closedday_text', 'pub_date']
    
    list_display = ('closedday_text', 'henryhub_text', 'wticushing_text', 'pub_date')
    list_filter = ['pub_date']

admin.site.register(Spot, SpotAdmin)