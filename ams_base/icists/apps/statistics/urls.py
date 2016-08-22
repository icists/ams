from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'icists.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.main),
    # url(r'^change-status/', 'icists.apps.statistics.views.change_status'),
    url(r'^query/([^/]+)/', views.get_data),
]
