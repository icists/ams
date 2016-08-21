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
    url(r'^email-check/$', 'icists.apps.session.views.email_check'),
    url(r'^univ-check/$', 'icists.apps.session.views.univ_check'),
    url(r'^univ-list/$', 'icists.apps.session.views.univ_list'),
    url(r'^changepw/$', 'icists.apps.session.views.changepw'),
    url(r'^changepw/(?P<uid>\w+)/$', 'icists.apps.session.views.changepw'),
]
