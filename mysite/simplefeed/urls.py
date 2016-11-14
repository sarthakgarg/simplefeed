from django.conf.urls import url
from . import views
from simplefeed.feeds import TargetFeed
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^register_show/$', views.register_show, name = 'register_show'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^login_show/$', views.login_show, name = 'login_show'),
    url(r'^login/$', views.loginuser, name = 'loginuser'),
    url(r'^logout/$', views.logoutuser, name = 'logoutuser'),
    url(r'^addform/$', views.addform, name = 'addform'),
    url(r'^add/$', views.add, name = 'add'),
    url(r'^(?P<target_id>[0-9]+)/updateform/$', views.updateform, name = 'updateform'),
    url(r'^(?P<target_id>[0-9]+)/update/$', views.update, name = 'update'),
    url(r'^(?P<target_id>[0-9]+)/delete/$', views.delete, name = 'delete'),
    url(r'^(?P<user_id>[0-9,A-Z,a-z]+)/rss/$', TargetFeed()),
]
