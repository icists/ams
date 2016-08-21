from django.contrib import admin
from icists.apps.policy.models import Configuration, Price
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class ConfigurationAdmin(ImportExportModelAdmin):
    list_display = ('application_stage', 'year')

    def has_add_permission(self, request):
        # if there's already an entry, do not allow adding
        count = Configuration.objects.all().count()
        if count == 0:
            return True
        else:
            return False


class PriceAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(Price, PriceAdmin)