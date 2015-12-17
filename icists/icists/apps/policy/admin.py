from django.contrib import admin
from icists.apps.policy.models import Configuration, Price
from import_export import resources
from import_export.admin import ImportExportModelAdmin



# Register your models here.
"""
class ConfigurationAdmin(ImportExportModelAdmin):
    list_display = ('application_stage', 'year')

class PriceAdmin(ImportExportModelAdmin):
    list_display = ('year', 'early_price_krw', 'early_price_usd', 'regular_price_krw', 'regular_price_usd', 'late_price_krw', 'late_price_usd', 'group_dc_usd', 'group_dc_krw')
    
admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(Price, PriceAdmin)
"""
