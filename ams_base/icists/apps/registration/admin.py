from django.contrib import admin
from django.contrib.auth.models import User
from icists.apps.session.models import UserProfile, University
from icists.apps.registration.models import \
    Application, Survey, EssayTopic, ProjectTopic, Participant, FullView
from icists.apps.policy.models import Configuration, Price
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

cnf = Configuration.objects.all()[0]
price = Price.objects.filter(year=cnf.year)[0]


# For application admin
def get_user_profile(obj):
    return UserProfile.objects.get(user=obj.user)


def make_pending(admin, request, qs):
    qs.update(screening_result='P')
make_pending.short_description = "Mark selected applications as pending"


def make_accepted(admin, request, qs):
    qs.update(screening_result='A')
make_accepted.short_description = "Mark selected applications as accepted"


def make_dismissed(admin, request, qs):
    qs.update(screening_result='D')
make_dismissed.short_description = "Mark selected applications as dismissed"


def make_embargo(admin, request, qs):
    qs.update(results_embargo=True)
make_embargo.short_description = "Embargo selected applications"


def make_not_embargo(admin, request, qs):
    qs.update(results_embargo=False)
make_not_embargo.short_description = "Cancel embargo selected applications"


def group_discount_true(admin, request, qs):
    qs.update(group_discount=True)
group_discount_true.short_description = 'set group discount : true'


def group_discount_false(admin, request, qs):
    qs.update(group_discount=False)
group_discount_false.short_description = 'set group discount : false'


def payment_status_paid(admin, request, qs):
    qs.update(payment_status='P')
payment_status_paid.short_description = 'set payment_status : PAID'


def payment_status_not_paid(admin, request, qs):
    qs.update(payment_status='N')
payment_status_not_paid.short_description = 'set payment_status : NOT_PAID'


def payment_status_over_paid(admin, request, qs):
    qs.update(payment_status='O')
payment_status_over_paid.short_description = 'set payment_status : OVER_PAID'


def payment_status_less_paid(admin, request, qs):
    qs.update(payment_status='L')
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
        universities = set([get_user_profile(u).university for
                            u in model_admin.model.objects.all()])
        return [(u.id, u.name) for u in universities]

    def queryset(self, request, qs):
        if self.value():
            return\
                qs.filter(user__userprofile__university__id__exact=self.value())
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
    univ_name = fields.Field()

    def dehydrate_univ_name(self, Application):
        try:
            userp = get_user_profile(Application)
            univ_code = userp.university
        except:
            print "ERROR"
            univ_code = "ERROR"
        return univ_code

    class Meta:
        model = Application
        fields = ('user__first_name', 'user__last_name',
                  'user__userprofile__gender',
                  'univ_name',
                  'user__userprofile__university', 'user__userprofile__major',
                  'user__userprofile__nationality', 'user__email',
                  'user__userprofile__phone', 'application_category',
                  'screening_result', 'project_topic', 'essay_topic',
                  'visa_letter_required', 'financial_aid',
                  'previously_participated')


class ApplicationAdmin(ImportExportModelAdmin):
    def get_user_info(self, obj):
        user = obj.user
        userp = get_user_profile(obj)
        return '%s %s (%s, %s): %s / %s - %s' %\
            (user.first_name, user.last_name, userp.gender, userp.birthday,
             userp.nationality, userp.university.name, userp.major)
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

    def get_gender(self, obj):
        return get_user_profile(obj).gender
    get_gender.admin_order_field = 'user__userprofile__gender'
    get_gender.short_description = "Gender"

    def get_submitted_status(self, obj):
        if obj.submit_time is not None:
            return 'Submitted'
        return 'Not Yet'
    get_submitted_status.admin_order_field = 'submit_time'
    get_submitted_status.short_description = 'Status'

    def get_address(self, obj):
        return "%s" %(get_user_profile(obj).address)
    get_address.short_description = 'Address'


    readonly_fields = ('get_user_info', 'get_address')
    fields = (('get_user_info', 'group_name'),
              ('application_category', 'submit_time'),
              ('screening_result', 'results_embargo'), 'project_topic',
              'project_topic_2nd', 'essay_topic', 'essay_text',
              ('visa_letter_required', 'financial_aid',
               'previously_participated', 'group_discount'),
              ('get_address'))
    list_display = ('get_name', 'get_gender', 'get_nationality', 'get_email',
                    'get_phone', 'application_category', 'get_submitted_status',
                    'screening_result', 'project_topic', 'project_topic_2nd',
                    'essay_topic', 'visa_letter_required', 'financial_aid',
                    'previously_participated', 'submit_time', 'group_discount')
    inlines = (SurveyInline, )

    list_filter = (StatusFilter, 'project_topic', 'project_topic_2nd',
                   'group_name', 'visa_letter_required', 'financial_aid',
                   'previously_participated', 'screening_result',
                   'application_category', UniversityFilter)

    actions = [make_pending, make_accepted, make_dismissed, make_embargo,
               make_not_embargo, group_discount_true, group_discount_false]
    resource_class = ApplicationResource


class ParticipantAdmin(ImportExportModelAdmin):

    def get_group_discount(self, obj):
        return obj.application.group_discount
    get_group_discount.admin_order_field = 'application__group_discount'
    get_group_discount.short_description = 'Group Discount'

    def recalculate_payment(self, request, qs):

        for q in qs:

            krw, usd = 0, 0
            application = q.application

            if application.application_category == 'E':
                krw += 100000
                usd += 95
            elif application.application_category == 'R':
                krw += 120000
                usd += 115
            elif application.application_category == 'L':
                krw += 140000
                usd += 135

            if application.group_discount:
                krw -= 20000
                usd -= 20

            if (q.accommodation_choice == 1):
                krw += 135000
                usd += 125
            elif (q.accommodation_choice == 2):
                krw += 180000
                usd += 165
            elif (q.accommodation_choice == 3):
                krw += 120000
                usd += 110
            elif (q.accommodation_choice == 4):
                krw += 112500
                usd += 105
            elif (q.accommodation_choice == 5):
                krw += 68000
                usd += 65

            if q.breakfast_option:
                krw += 20000
                usd += 20
            if q.pretour:
                krw += 40000
                usd += 30
            if q.posttour:
                krw += 100000
                usd += 90

            q.required_payment_krw = krw
            q.required_payment_usd = usd
            q.save()

    recalculate_payment.short_description = 'recalculate required payment'

    def get_user_info(self, obj):
        application = obj.application
        user = application.user
        userp = UserProfile.objects.get(user=user)
        return '%s %s (%s, %s): %s / %s - %s' %\
            (user.first_name, user.last_name, userp.gender, userp.birthday,
             userp.nationality, userp.university.name, userp.major)
    get_user_info.short_description = 'User Info'

    def get_name(self, obj):
        return obj.application.user.first_name + ' ' + \
            obj.application.user.last_name
    get_name.admin_order_field = 'user__first_name'
    get_name.short_description = 'Name'

    def get_gender(self, obj):
        user = obj.application.user
        userp = UserProfile.objects.get(user=user)
        return userp.gender
    get_gender.admin_order_field = 'user__gender'
    get_gender.short_description = 'Gender'

    def get_email(self, obj):
        application = obj.application
        user = application.user
        return user.email
    get_email.admin_order_field = 'user__email'
    get_email.short_description = 'Email'

    def get_payment_krw(self, obj):
        krw, usd = obj.payment()
        return int(krw)
    get_payment_krw.short_description = 'Payment in KRW'

    def get_payment_usd(self, obj):
        krw, usd = obj.payment()
        return int(usd)
    get_payment_usd.short_description = 'Payment in USD'

    readonly_fields =\
        ('get_name', 'get_gender', 'get_payment_krw', 'get_payment_usd')
    fields = (
        ('get_name', 'get_gender'),
        # ('get_user_info'),
        ('accommodation_choice'),
        ('project_team_no'),
        ('payment_status', 'payment_option', 'remitter_name'),
        ('get_payment_krw', 'get_payment_usd'),
        ('breakfast_option', 'dietary_option'),
        ('pretour', 'posttour'),
    )
    list_display = ('get_name', 'get_gender', 'get_email', 'get_group_discount',
                    'accommodation_choice', 'project_team_no', 'payment_status',
                    'payment_option', 'required_payment_krw',
                    'required_payment_usd', 'remitter_name', 'breakfast_option',
                    'dietary_option', 'pretour', 'posttour', 'submit_time')
    list_filter = ('accommodation_choice', 'payment_status', 'payment_option')
    actions = [payment_status_paid, payment_status_not_paid,
               payment_status_over_paid, payment_status_less_paid,
               'recalculate_payment']


class ParticipantResource(resources.ModelResource):
    class Meta:
        model = Participant


class FullViewAdmin(ImportExportModelAdmin):
    list_max_show_all = 500
    list_per_page = 500
    list_display=('first_name', 'last_name', 'email', 'application_category',\
                  'nationality', 'gender', 'project_topic_id', \
                  'project_team_no', 'breakfast_option', 'accommodation_id', \
                  'required_payment_krw', 'required_payment_usd')
    # note : the foreignkey fields are not displayed properly.

class FullViewResource(resources.ModelResource):
    class Meta:
        model = FullView



admin.site.register(FullView, FullViewAdmin)
admin.site.register(EssayTopic, EssayTopicAdmin)
admin.site.register(ProjectTopic, ProjectTopicAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Participant, ParticipantAdmin)
