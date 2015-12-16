from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

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
    # submit_status = models.BooleanField(default=False)
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
        ForeignKey(ProjectTopic, related_name='application_project_2nd')
    essay_topic = models.ForeignKey(EssayTopic,
                                    related_name='application_essay')
    essay_text = models.TextField()
    visa_letter_required = models.CharField(max_length=1,
                                            choices=YESNO, default='N')
    financial_aid = models.CharField(max_length=1, choices=YESNO, default='N')
    # year = models.IntegerField(default=2015)   # Use last_updated_time
    user = models.ForeignKey(User, related_name='application')
    # user = models.OneToOneField(User, related_name='application')
    group_name = models.CharField(max_length=45, blank=True)
    group_discount = models.BooleanField(default=False)
    previously_participated = models.CharField(max_length=1,
                                               choices=YESNO, default='N')
    last_updated_time = models.DateTimeField(auto_now=True)
    submit_time = models.DateTimeField(null=True)

    '''
    def save(self, *args, **kwargs):
        if not self.pk:
            slef.application_category = settings.APPLICATION_CATEGORY
        super(Application, self).save(*args, **kwargs)
    '''


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
        (1, 'Standard Ondol'),
        (2, 'Standard Ondol Twin'),
        (3, 'Deluxe Ondol'),
        (4, 'Suite Ondol'),
        (5, 'KAIST Dormitory'),
        (6, 'No Accommodation'),
    )

    accommodation = models.ForeignKey('Accommodation',
                                      related_name="participant", null=True)
    accommodation_choice = models.IntegerField(choices=ACCOMMODATION_CHOICES)
    is_accommodation_assigned = models.BooleanField(default=False)
    application = models.OneToOneField('Application',
                                       related_name="participant")
    discount = models.ForeignKey('Discount',
                                 related_name="participant", null=True)

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


class Accommodation(models.Model):
    hotel_name = models.CharField(max_length=45)
    hotel_room = models.CharField(max_length=45)
    accommodation_payment = models.IntegerField()
    gender = models.CharField(max_length=45)
    availability = models.IntegerField()


class Discount(models.Model):
    discount_code = models.CharField(max_length=10, primary_key=True)
    discount_value = models.IntegerField()
    disocunt_percent = models.FloatField()


class Survey(models.Model):
    application = models.ForeignKey("Application", related_name='survey')
    q1 = models.TextField(default='', blank=True, null=True)
    q2 = models.TextField(default='', blank=True, null=True)
    q3 = models.TextField(default='', blank=True, null=True)
    q4 = models.TextField(default='', blank=True, null=True)
    q5 = models.TextField(default='', blank=True, null=True)
    q6 = models.TextField(default='', blank=True, null=True)
    q7 = models.TextField(default='', blank=True, null=True)
    q8 = models.TextField(default='', blank=True, null=True)
    q9 = models.TextField(default='', blank=True, null=True)
    q10 = models.TextField(default='', blank=True, null=True)
