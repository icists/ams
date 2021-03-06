from django.db import models

# Create your models here.


class Configuration(models.Model):
    """ describes the current configuration status """

    # application_stage
    BEFORE_EARLY = 'BE'
    EARLY = 'E'
    EARLY_CLOSED = 'EC'
    REGULAR = 'R'
    REGULAR_CLOSED = 'RC'
    LATE = 'L'
    LATE_CLOSED = 'LC'

    APPLICATION_STAGE = (
        (BEFORE_EARLY, 'Before Early'),
        (EARLY, 'Early'),
        (EARLY_CLOSED, 'Early Closed'),
        (REGULAR, 'Regular'),
        (REGULAR_CLOSED, 'Regular Closed'),
        (LATE, 'Late'),
        (LATE_CLOSED, 'Late Closed'),
    )

    application_stage = \
        models.CharField(max_length=2,
                         choices=APPLICATION_STAGE,
                         default=BEFORE_EARLY)
    year = models.IntegerField()

class PaymentInfo(models.Model):
    bank_name =  models.CharField(max_length=100)
    bank_branch =  models.CharField(max_length=100)
    account_number =  models.CharField(max_length=100)
    recipient_name =  models.CharField(max_length=100)
    swift_code =  models.CharField(max_length=100)

class Price(models.Model):
    """ the price and the discount rate each year. """
    year = models.IntegerField()
    early_price_krw = models.IntegerField()
    early_price_usd = models.IntegerField()
    regular_price_krw = models.IntegerField()
    regular_price_usd = models.IntegerField()
    late_price_krw = models.IntegerField()
    late_price_usd = models.IntegerField()
    group_dc_krw = models.IntegerField()
    group_dc_usd = models.IntegerField()
    breakfast_krw = models.IntegerField()
    breakfast_usd = models.IntegerField()
    pretour_krw = models.IntegerField()
    pretour_usd = models.IntegerField()
    posttour_krw = models.IntegerField()
    posttour_usd = models.IntegerField()

class AccommodationOption(models.Model):
    option_name = models.CharField(max_length=45)
    capacity_per_room = models.IntegerField()
    total_capacity = models.IntegerField()
    fee_krw = models.IntegerField()
    fee_usd = models.IntegerField()

    def __str__(self):
        return '[{}] {} - Capacity : {} people / Price : USD {}, KRW {}'.format(self.id, self.option_name, self.capacity_per_room, self.fee_usd, self.fee_krw)

