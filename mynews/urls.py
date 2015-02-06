from django.conf.urls import patterns, url

from mynews import views, receivers

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^today/$', views.today, name='today'),
    url(r'^(?P<news_id>\d+)/$', views.detail, name='detail'),
    url(r'^prev/$',  views.prev, name='prev' ),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
#    # ex: /polls/5/results/
#    url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
#    # ex: /polls/5/vote/
#    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),

#    url(r'^$', views.IndexView.as_view(), name='index'),
#    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
)