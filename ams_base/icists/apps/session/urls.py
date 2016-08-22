from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'icists.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.main),
    url(r'^profile/$', views.profile),
    url(r'^profile/(?P<uid>\w+)/$', views.profile),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^signup/$', views.signup),
    url(r'^email-check/$', views.email_check),
    url(r'^univ-check/$', views.univ_check),
    url(r'^univ-list/$', views.univ_list),
    url(r'^changepw/$', views.changepw),
    url(r'^changepw/(?P<uid>\w+)/$', views.changepw),
]
