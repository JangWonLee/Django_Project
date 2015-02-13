from django.contrib import admin
from mynews.models import News, Comments, Spot, Activities, Clippings

class CommentsInline(admin.TabularInline):
    model = Comments
    extra = 1

class NewsAdmin(admin.ModelAdmin):
    fields = ['link_text', 'title_text', 'summary_text', 'opinion_text', 'pub_date']

    list_display = ('link_text', 'title_text', 'summary_text', 'opinion_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['title_text']
    
    inlines = [CommentsInline]

admin.site.register(News, NewsAdmin)
#admin.site.register(Comments)

class SpotAdmin(admin.ModelAdmin):
    fields = ['henryhub_text', 'wticushing_text', 'closedday_text', 'pub_date']
    
    list_display = ('closedday_text', 'henryhub_text', 'wticushing_text', 'pub_date')
    list_filter = ['pub_date']

admin.site.register(Spot, SpotAdmin)

#tag 1 = comment
class ActivitiesAdmin(admin.ModelAdmin):
    fields = ['publisher_text', 'title_text', 'pub_date', 'comment_text', 'tag']
    
    list_display = ('tag', 'pub_date', 'publisher_text', 'title_text', 'comment_text')
    list_filter = ['pub_date']

admin.site.register(Activities,ActivitiesAdmin)

class ClippingsAdmin(admin.ModelAdmin):
    fields = ['user', 'news', 'pub_date']
    
    list_display = ('user', 'news', 'pub_date')
    list_filter = ['user']
    
admin.site.register(Clippings, ClippingsAdmin)