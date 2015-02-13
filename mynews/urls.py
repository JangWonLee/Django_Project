from django.conf.urls import patterns, url
from mynews import receivers
from mynews import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^activity/$', views.activity, name='activity'),
    url(r'^today/$', views.today, name='today'),
    url(r'^(?P<news_id>\d+)/$', views.detail, name='detail'),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^clipping/$', views.clipping, name='clipping'),
    
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    
    url(r'^comment_edit/$', views.comment_edit, name='comment_edit'),
    
    url(r'^news_clip/$', views.news_clip, name='news_clip'),
    url(r'^news_clip_cancel/$', views.news_clip_cancel, name='news_clip_cancel'),
    url(r'^comment_delete/$', views.comment_delete, name='comment_delete'),
    url(r'^comment_post/$', views.comment_post, name='comment_post'),
    

#    url(r'^$', views.IndexView.as_view(), name='index'),
#    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
)
