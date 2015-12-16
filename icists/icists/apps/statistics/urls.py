from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'icists.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'icists.apps.statistics.views.main'),
    url(r'^change-status/', 'icists.apps.statistics.views.change_status'),
    url(r'^query/([^/]+)/', 'icists.apps.statistics.views.get_data'),
]
