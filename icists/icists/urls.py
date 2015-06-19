from django.conf.urls import include, url, handler400, handler403, handler404, handler500
from django.contrib import admin
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
from django.views.generic import RedirectView

urlpatterns = [
    # Examples:
    # url(r'^$', 'icists.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include('icists.apps.registration.urls')),
    url(r'^registration/', include('icists.apps.registration.urls')),
    url(r'^session/', include('icists.apps.session.urls')),
    url(r'^statistic/', include('icists.apps.statistic.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]

handler400 = lambda request: render(request, 'error/400.html')
handler403 = lambda request: render(request, 'error/403.html')
handler404 = lambda request: render(request, 'error/404.html')
handler500 = lambda request: render(request, 'error/500.html')
