from django.contrib import admin
from django.contrib.auth.models import User
from icists.apps.session.models import UserProfile
from icists.apps.registration.models import Application
from icists.apps.registration.models import Survey

# Register your models here.

def get_user_profile(obj):
    return UserProfile.objects.get(user=obj.user)

class SurveyInline(admin.StackedInline):
    model = Survey
    can_delete = False
    max_num = 1
    extra = 0

class ApplicationAdmin(admin.ModelAdmin):
    def get_user_info(self, obj):
        user = obj.user
        userp = get_user_profile(obj)
        return '%s %s (%s, %s): %s / %s - %s' % (user.first_name, user.last_name, userp.gender, userp.birthday, userp.nationality, userp.university, userp.major)
    get_user_info.short_description = 'User Info'
    
    def get_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name
    get_name.admin_order_field = 'user__first_name'
    get_name.short_description = 'Name'

    def get_nationality(self, obj):
        return get_user_profile(obj).nationality
    get_nationality.admin_order_field = 'user__userprofile__nationality'
    get_nationality.short_description = 'Nationality'

    def get_email(self, obj):
        return obj.user.email
    get_email.admin_order_field = 'user__email'
    get_email.short_description = 'Email'

    def get_phone(self, obj):
        return get_user_profile(obj).phone
    get_phone.admin_order_field = 'user__userprofile__phone'
    get_phone.short_description = 'Phone'

    readonly_fields = ('get_user_info', )
    fields = (('get_user_info', 'group_name'), ('application_category', 'submit_time'), ('screening_result', 'results_embargo'), 'project_topic', 'essay_topic', 'essay_text', ('visa_letter_required', 'financial_aid', 'previously_participated'))
    list_display = ('get_name', 'get_nationality', 'get_email', 'get_phone', 'application_category', 'screening_result', 'project_topic', 'essay_topic', 'visa_letter_required', 'financial_aid', 'previously_participated')
    inlines = (SurveyInline, )
    
    list_filter = ('project_topic', 'visa_letter_required', 'financial_aid', 'previously_participated', 'screening_result', 'application_category', 'user__userprofile__university')

admin.site.register(Application, ApplicationAdmin)
