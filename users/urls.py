from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required


from users import views

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^(?P<pk>\d+)/$', views.UserView.as_view(), name='userview'),
    url(r'^login/$', views.login, name='loginpage'), 
    url(r'^logout/$', views.logout, name='logoutpage'),
    url(r'^search-user/$', login_required(views.search_user), name='searchuser'),
    url(r'^accept-or-decline/(?P<requester_id>\d+)/$', views.accept_or_decline, name='acceptordecline'),
    url(r'^send-request/(?P<requestee_id>\d+)/$', views.send_request, name='sendrequest'),
    #url(r'^signup/$', views.sign_up, name='signup'),
)