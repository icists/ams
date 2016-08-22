from django.conf.urls import url
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'icists.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.main),
    url(r'^application/$', views.application),
    url(r'^submit/$', views.submit),
    url(r'^financial/$', views.financial),
    url(r'^cancel/$', views.cancel),
    url(r'^participation/$', views.participation),

    # url(r'^change-status/(?P<uid>\w+)/$',
    #     'icists.apps.registration.views.change_status',),
]
