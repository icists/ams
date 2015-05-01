from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'icists.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'icists.apps.session.views.main'),
    url(r'^profile/$', 'icists.apps.session.views.profile'),
    url(r'^profile/(?P<uid>\w+)/$', 'icists.apps.session.views.profile',),
    url(r'^login/$', 'icists.apps.session.views.login'),
    url(r'^logout/$', 'icists.apps.session.views.logout'),
    url(r'^signup/$', 'icists.apps.session.views.signup'),
]
