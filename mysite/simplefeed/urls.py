from django.conf.urls import url
from . import views
from simplefeed.feeds import TargetFeed
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^addform/$', views.addform, name = 'addform'),
    url(r'^add/$', views.add, name = 'add'),
    url(r'^(?P<target_id>[0-9]+)/updateform/$', views.updateform, name = 'updateform'),
    url(r'^(?P<target_id>[0-9]+)/update/$', views.update, name = 'update'),
    url(r'^(?P<target_id>[0-9]+)/delete/$', views.delete, name = 'delete'),
    url(r'^rss/$', TargetFeed()),
]
