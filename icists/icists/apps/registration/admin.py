from django.contrib import admin
from django.contrib.auth.models import User
from icists.apps.session.models import UserProfile
from icists.apps.registration.models import Application, Survey, EssayTopic, ProjectTopic, Participant
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

# For application admin
def get_user_profile(obj):
    return UserProfile.objects.get(user=obj.user)

def make_pending(admin, request, qs):
    qs.update(screening_result = 'P')
make_pending.short_description = "Mark selected applications as pending"

def make_accepted(admin, request, qs):
    qs.update(screening_result = 'A')
make_accepted.short_description = "Mark selected applications as accepted"

def make_dismissed(admin, request, qs):
    qs.update(screening_result = 'D')
make_dismissed.short_description = "Mark selected applications as dismissed"

def make_embargo(admin, request, qs):
    qs.update(results_embargo = True)
make_embargo.short_description = "Embargo selected applications"

def make_not_embargo(admin, request, qs):
    qs.update(results_embargo = False)
make_not_embargo.short_description = "Cancel embargo selected applications"

def group_discount_true(admin, request, qs):
    qs.update(group_discount=True);
group_discount_true.short_description = 'set group discount : true'
def group_discount_false(admin, request, qs):
    qs.update(group_discount=False);
group_discount_false.short_description = 'set group discount : false'

def payment_status_paid(admin, request, qs):
    qs.update(payment_status='P');
payment_status_paid.short_description = 'set payment_status : PAID'
def payment_status_not_paid(admin, request, qs):
    qs.update(payment_status='N');
payment_status_not_paid.short_description = 'set payment_status : NOT_PAID'
def payment_status_over_paid(admin, request, qs):
    qs.update(payment_status='O');
payment_status_over_paid.short_description = 'set payment_status : OVER_PAID'
def payment_status_less_paid(admin, request, qs):
    qs.update(payment_status='L');
payment_status_less_paid.short_description = 'set payment_status : LESS_PAID'

class StatusFilter(admin.SimpleListFilter):
    title = 'submitted status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Submitted'),
            ('no', 'Not Yet'),
        )

    def queryset(self, request, qs):
        if self.value() == 'yes':
            return qs.filter(submit_time__isnull=False)

        if self.value() == 'no':
            return qs.filter(submit_time__isnull=True)

class UniversityFilter(admin.SimpleListFilter):
    title = 'university'
    parameter_name = 'university'

    def lookups(self, request, model_admin):
        universities = set([get_user_profile(u).university for u in model_admin.model.objects.all()])
        return [(u.id, u.name) for u in universities]

    def queryset(self, request, qs):
        if self.value():
            return qs.filter(user__userprofile__university__id__exact=self.value())
        else:
            return qs


class ProjectTopicAdmin(admin.ModelAdmin):
    list_display = ('year', 'number', 'text')
    list_filter = ('year',)


class EssayTopicAdmin(admin.ModelAdmin):
    list_display = ('year', 'number', 'text', 'description')
    list_filter = ('year',)


class SurveyInline(admin.StackedInline):
    model = Survey
    can_delete = False
    max_num = 1
    extra = 0


class ApplicationResource(resources.ModelResource):
    class Meta:
        model = Application
        #fields = ('get_name', 'get_nationality', 'get_email', 'get_phone', 'application_category', 'screening_result', 'project_topic', 'essay_topic', 'visa_letter_required', 'financial_aid', 'previously_participated')
        fields = ('user__first_name', 'user__last_name', 'user__userprofile__nationality', 'user__email', 'user__userprofile__phone', 'application_category', 'screening_result', 'project_topic', 'essay_topic', 'visa_letter_required', 'financial_aid', 'previously_participated')


class ApplicationAdmin(ImportExportModelAdmin):
    def get_user_info(self, obj):
        user = obj.user
        userp = get_user_profile(obj)
        return '%s %s (%s, %s): %s / %s - %s' % (user.first_name, user.last_name, userp.gender, userp.birthday, userp.nationality, userp.university.name, userp.major)
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

    def get_submitted_status(self, obj):
        if obj.submit_time != None:
            return 'Submitted'
        return 'Not Yet'
    get_submitted_status.admin_order_field = 'submit_time'
    get_submitted_status.short_description = 'Status'

    readonly_fields = ('get_user_info', )
    fields = (('get_user_info', 'group_name'), ('application_category', 'submit_time'), ('screening_result', 'results_embargo'), 'project_topic', 'project_topic_2nd', 'essay_topic', 'essay_text', ('visa_letter_required', 'financial_aid', 'previously_participated', 'group_discount'))
    list_display = ('get_name', 'get_nationality', 'get_email', 'get_phone', 'application_category', 'get_submitted_status', 'screening_result', 'project_topic', 'project_topic_2nd', 'essay_topic', 'visa_letter_required', 'financial_aid', 'previously_participated', 'submit_time', 'group_discount')
    inlines = (SurveyInline, )

    list_filter = (StatusFilter, 'project_topic', 'project_topic_2nd', 'group_name', 'visa_letter_required', 'financial_aid', 'previously_participated', 'screening_result', 'application_category', UniversityFilter)

    actions = [make_pending, make_accepted, make_dismissed, make_embargo, make_not_embargo, group_discount_true, group_discount_false]
    resource_class = ApplicationResource


class ParticipantAdmin(ImportExportModelAdmin):
    def get_user_info(self, obj):
        application = obj.application
        user = application.user
        userp = UserProfile.objects.get(user=user)
        return '%s %s (%s, %s): %s / %s - %s' % (user.first_name, user.last_name, userp.gender, userp.birthday, userp.nationality, userp.university.name, userp.major)
    get_user_info.short_description = 'User Info'

    def get_name(self, obj):
        return obj.application.user.first_name + ' ' + obj.application.user.last_name
    get_name.admin_order_field = 'user__first_name'
    get_name.short_description = 'Name'

    def get_email(self, obj):
        application = obj.application
        user = application.user
        return user.email
    get_email.admin_order_field = 'user__email'
    get_email.short_description = 'Email'

    readonly_fields = ('required_payment_krw', 'required_payment_usd', 'get_name')
    fields =    (   ('get_name'),
                    #('get_user_info'),
                    ('accommodation_choice'),
                    ('project_team_no'),
                    ('payment_status', 'payment_option', 'remitter_name'),
                    ('required_payment_krw', 'required_payment_usd'),
                    ('breakfast_option', 'dietary_option'),
                    ('pretour', 'posttour'),
                )
    list_display = ('get_name', 'get_email', 'accommodation_choice', 'project_team_no', 'payment_status', 'payment_option', 'required_payment_krw', 'required_payment_usd', 'remitter_name', 'breakfast_option',
                            'dietary_option', 'pretour', 'posttour', 'submit_time')
    list_filter = ('accommodation_choice', 'payment_status', 'payment_option')
    actions = [payment_status_paid, payment_status_not_paid, payment_status_over_paid, payment_status_less_paid]

class ParticipantResource(resources.ModelResource):
    class Meta:
        model = Participant



admin.site.register(EssayTopic, EssayTopicAdmin)
admin.site.register(ProjectTopic, ProjectTopicAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Participant, ParticipantAdmin)
