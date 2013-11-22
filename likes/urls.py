from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from likes import views

urlpatterns = patterns('',
    url(r'^(?P<postid>\d+)/(?P<userid>\d+)/$', views.add_like, name='addlike'),
)