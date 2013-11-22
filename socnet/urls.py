from django.conf.urls import patterns, include, url
from users.api import UserResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

user_resource = UserResource()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'socnet.views.home', name='home'),
    # url(r'^socnet/', include('socnet.foo.urls')),
    url(r'^', include('users.urls', namespace='users')),
    url(r'^likes/', include('likes.urls', namespace='likes')),
    url(r'^', include('signup.urls', namespace='signup')),
    url(r'^api/', include(user_resource.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # Notes: obfuscate the admin/ page or something to increase security
    url(r'^admin/', include(admin.site.urls)),
)