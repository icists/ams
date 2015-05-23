from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from icists.apps.session.models import UserProfile
# Register your models here.

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user profile'

def get_user_profile(obj):
    return UserProfile.objects.get(user=obj)

class UserAdmin(admin.ModelAdmin):
    def get_name(self, obj):
        return obj.first_name + ' ' + obj.last_name
    get_name.admin_order_field = 'user__first_name'
    get_name.short_description = 'Name'

    def get_university(self, obj):
        return get_user_profile(obj).university
    get_university.admin_order_field = 'userprofile__university'
    get_university.short_description = 'University'
    
    def get_major(self, obj):
        return get_user_profile(obj).major
    get_major.admin_order_field = 'userprofile__major'
    get_major.short_description = 'Major'

    def get_phone(self, obj):
        return get_user_profile(obj).phone
    get_phone.admin_order_field = 'userprofile__phone'
    get_phone.short_description = 'Phone'

    list_display = ('get_name', 'get_university', 'get_major', 'email', 'get_phone', 'is_staff')
    inlines = (UserProfileInline, )
    
    #list_filter = ('project_topic', 'visa_letter_required', 'financial_aid', 'previously_participated', 'screening_result', 'application_category', 'user__userprofile__university')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
