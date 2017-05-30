from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from icists.apps.policy.models import Configuration, Price
cnf = Configuration.objects.first()
price = Price.objects.filter(year=cnf.year).first()

# Create your models here.

class EssayTopic(models.Model):
    year = models.IntegerField()
    number = models.IntegerField()
    text = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return "(%d) %d. %s" % (self.year, self.number, self.text)


class ProjectTopic(models.Model):
    year = models.IntegerField()
    number = models.IntegerField()
    text = models.CharField(max_length=100)

    def __unicode__(self):
        return "(%d) %d. %s" % (self.year, self.number, self.text)


class Application(models.Model):
    EARLY = 'E'
    REGULAR = 'R'
    LATE = 'L'
    APPLICATION_CATEGORY = (
        (EARLY, 'Early'),
        (REGULAR, 'Regular'),
        (LATE, 'Late'),
    )
    ACCEPTED = 'A'
    DISMISSED = 'D'
    PENDING = 'P'
    SCREENING_RESULT = (
        (ACCEPTED, 'Accepted'),
        (DISMISSED, 'Dismissed'),
        (PENDING, 'Pending'),
    )

    YESNO = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    application_category = models.CharField(max_length=1,
                                            choices=APPLICATION_CATEGORY,
                                            default=REGULAR)
    screening_result = models.CharField(max_length=1,
                                        choices=SCREENING_RESULT,
                                        default=PENDING)
    results_embargo = models.BooleanField(default=True)
    project_topic = models.ForeignKey(ProjectTopic,
                                      related_name='application_project')
    project_topic_2nd = models.\
        ForeignKey(ProjectTopic, related_name='application_project_2nd',
                   blank=True, null=True)
    essay_topic = models.ForeignKey(EssayTopic,
                                    related_name='application_essay')
    essay_text = models.TextField()
    visa_letter_required = models.CharField(max_length=1,
                                            choices=YESNO, default='N')
    financial_aid = models.CharField(max_length=1, choices=YESNO, default='N')
    user = models.ForeignKey(User, related_name='application')
    group_name = models.CharField(max_length=45, blank=True)
    group_discount = models.BooleanField(default=False)
    previously_participated = models.CharField(max_length=1,
                                               choices=YESNO, default='N')
    last_updated_time = models.DateTimeField(auto_now=True)
    submit_time = models.DateTimeField(null=True)

    def payment(self):
        krw, usd = 0, 0
        if self.application_category == 'E':
            krw += price.early_price_krw
            usd += price.early_price_usd
        if self.application_category == 'R':
            krw += price.regular_price_krw
            usd += price.regular_price_usd
        if self.application_category == 'L':
            krw += price.late_price_krw
            usd += price.late_price_usd
        if self.group_discount == True:
            krw -= price.group_dc_krw
            usd -= price.group_dc_usd
        return (krw, usd)


class Participant(models.Model):
    NOT_PAID = 'N'
    PAID = 'P'
    LESS_PAID = 'L'
    OVER_PAID = 'O'
    PAYMENT_STATUS = (
        (NOT_PAID, 'Not Paid'),
        (PAID, 'Paid'),
        (LESS_PAID, 'Less Paid'),
        (OVER_PAID, 'Over Paid'),
    )
    PAYPAL = 'P'
    BANK_TRANSFER = 'B'
    PAYMENT_OPTIONS = (
        (PAYPAL, 'Paypal'),
        (BANK_TRANSFER, 'Bank Transfer'),
    )
    ACCOMMODATION_CHOICES = (
        (1, 'Triple'),
        (2, 'Double Twin'),
        (3, 'Superior Ondol'),
        (4, 'Deluxe Ondol'),
        (5, 'No Accommodation'),
    )

    accommodation_choice = models.IntegerField(choices=ACCOMMODATION_CHOICES)
    is_accommodation_assigned = models.BooleanField(default=False)
    application = models.OneToOneField('Application',
                                       related_name="participant")

    project_team_no = models.PositiveSmallIntegerField()
    payment_status = models.CharField(max_length=1,
                                      choices=PAYMENT_STATUS, default=NOT_PAID)
    payment_option = models.CharField(max_length=1,
                                      choices=PAYMENT_OPTIONS, default=PAYPAL)
    required_payment_krw = models.IntegerField()
    required_payment_usd = models.IntegerField()
    remitter_name = models.CharField(max_length=45, null=True, blank=True)
    breakfast_option = models.BooleanField(default=False)
    # dietary_option := Vegetarian, Halal, Others (Optional text input)
    dietary_option = models.CharField(max_length=45, null=True, blank=True)
    pretour = models.BooleanField(default=False)
    posttour = models.BooleanField(default=False)
    group_discount = models.BooleanField(default=False)
    submit_time = models.DateTimeField(null=True)

    def payment(self):
        krw, usd = self.application.payment()

        accommodation = self.accommodation_choice
        if accommodation == 1:
            krw += 187000
            usd += 160
        elif accommodation == 2:
            krw += 141000
            usd += 120
        elif accommodation == 3:
            krw += 126000
            usd += 110
        elif accommodation == 4:
            krw += 90000
            usd += 77
        if self.breakfast_option:
            krw += price.breakfast_krw
            usd += price.breakfast_usd
        if self.pretour:
            krw += price.pretour_krw
            usd += price.pretour_usd
        if self.posttour:
            krw += price.posttour_krw
            usd += price.posttour_usd
        return (krw, usd)


class Survey(models.Model):
    application = models.ForeignKey("Application", related_name='survey')
    q1 = models.TextField(default='', blank=True, null=True)
    q2 = models.TextField(default='', blank=True, null=True)
    q3 = models.TextField(default='', blank=True, null=True)
    q4 = models.TextField(default='', blank=True, null=True)


class FullView(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(blank=True)
    app = models.ForeignKey(Application, related_name='full_view', on_delete=models.DO_NOTHING)
    part = models.ForeignKey(Participant, related_name='full_view', on_delete=models.DO_NOTHING)
    application_category = models.CharField(max_length=1)
    nationality = models.CharField(max_length=45)
    gender = models.CharField(max_length=45)
    project_topic_id = models.IntegerField()
    project_team_no = models.PositiveSmallIntegerField()
    accommodation_id = models.IntegerField()
    breakfast_option = models.BooleanField(default=False)
    required_payment_krw = models.IntegerField()
    required_payment_usd = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'full_view'
