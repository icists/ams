from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'icists.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'icists.apps.statistic.views.main'),
]
