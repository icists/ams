from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'icists.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'icists.apps.registration.views.main'),
    url(r'^application/$', 'icists.apps.registration.views.application'),
    url(r'^submit/$', 'icists.apps.registration.views.submit'),
    url(r'^financial/$', 'icists.apps.registration.views.financial'),
    url(r'^cancel/$', 'icists.apps.registration.views.cancel'),
    url(r'^participant/$', 'icists.apps.registration.views.participant'),
    #url(r'^admin-view/$', 'icists.apps.registration.views.admin_view'),
    #url(r'^admin-view/(?P<uid>\w+)/$', 'icists.apps.registration.views.admin_view',),
    #url(r'^change-status/(?P<uid>\w+)/$', 'icists.apps.registration.views.change_status',),
]
