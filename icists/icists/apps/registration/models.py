from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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

    #submit_status = models.BooleanField(default=False)
    application_category = models.CharField(max_length=1,
                                            choices=APPLICATION_CATEGORY, default=EARLY)
    screening_result = models.CharField(max_length=1,
                                        choices=SCREENING_RESULT, default=PENDING)
    results_embargo = models.BooleanField(default=True)
    project_topic = models.CharField(max_length=45)
    essay_topic = models.CharField(max_length=500)
    essay_text = models.TextField()
    visa_letter_required = models.BooleanField(default=False)
    financial_aid = models.BooleanField(default=False)
    #year = models.IntegerField(default=2015)   # Use last_updated_time
    user = models.ForeignKey(User, related_name='application')
    #user = models.OneToOneField(User, related_name='application')
    group_name = models.CharField(max_length=45, blank=True)
    previously_participated =  models.BooleanField(default=False)
    last_updated_time = models.DateTimeField(auto_now=True)
    submit_time = models.DateTimeField(null=True)


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

    accommodation = models.ForeignKey('Accommodation', related_name="participant")
    application = models.OneToOneField('Application', related_name="participant")
    discount = models.ForeignKey('Discount', related_name="participant")

    project_team_no = models.PositiveSmallIntegerField()
    payment_status = models.CharField(max_length=1,
                                      choices=PAYMENT_STATUS, default=NOT_PAID)
    required_payment = models.IntegerField()
    breakfast_option = models.BooleanField(default=False)
    dietary_option = models.CharField(max_length=45) # Vegetarian, Halal, Others (Optional text input)
    pretour = models.BooleanField(default=False)
    posttour = models.BooleanField(default=False)


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
    q1 = models.TextField(blank=True)
    q2 = models.TextField(blank=True)
    q3 = models.TextField(blank=True)
    q4 = models.TextField(blank=True)
    q5 = models.TextField(blank=True)
    q6 = models.TextField(blank=True)
    q7 = models.TextField(blank=True)
    q8 = models.TextField(blank=True)
    q9 = models.TextField(blank=True)
    q10 = models.TextField(blank=True)
