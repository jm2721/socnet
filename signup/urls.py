from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from signup import views

urlpatterns = patterns('',
    url(r'^signup/$', views.sign_up, name='signup'),
    url(r'^activate/$', views.activate, name='activate'),
)