from django.contrib import admin

from icists.apps.registration.models import Application
from icists.apps.registration.models import Survey

# Register your models here.


admin.site.register(Application)
admin.site.register(Survey)
