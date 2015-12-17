from django.contrib import admin
from icists.apps.policy.models import Configuration, Price
from import_export import resources
from import_export.admin import ImportExportModelAdmin



# Register your models here.
class ConfigurationAdmin(ImportExportModelAdmin):
    list_display = ('application_stage', 'year')

class PriceAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(Price, PriceAdmin)
