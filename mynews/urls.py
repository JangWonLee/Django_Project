from django.conf.urls import patterns, url

from mynews import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^activity/$', views.activity, name='activity'),
    url(r'^today/$', views.today, name='today'),
    url(r'^(?P<news_id>\d+)/$', views.detail, name='detail'),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^(?P<comment_id>\d+)/cdelete/$', views.comment_delete, name='comment_delete'),
    url(r'^cedit/$', views.comment_edit, name='comment_edit'),
    

#    url(r'^$', views.IndexView.as_view(), name='index'),
#    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
)
