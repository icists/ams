from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponse

urlpatterns = [
    # Examples:
    # url(r'^$', 'icists.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', lambda request: HttpResponse('Hello, World!')),
    url(r'^registration/', include('icists.apps.registration.urls')),
    url(r'^session/', include('icists.apps.session.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
