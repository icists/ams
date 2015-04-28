from django.db import models

# Create your models here.

class Application(models.Model):
    ApplicationNo = models.AutoField(primary_key=True)
    SubmitStatus = models.CharField(max_length = 45) #Draft/Submitted
    ApplicationCategory = models.CharField(max_length = 45) #Early/Regular/Late
    ScreeningResults = models.CharField(max_length = 45) #Accepted/Dismissed/Pending(Default)
    Email = models.CharField(max_length = 45)
    Password = models.CharField(max_length = 45)
    FirstName = models.CharField(max_length = 45)
    LastName = models.CharField(max_length = 45)
    Birthday = models.DateField()
    Nationality = models.CharField(max_length = 45)
    Gender = models.CharField(max_length = 45)
    Phone = models.CharField(max_length = 45) #country_code + number
    Major = models.CharField(max_length = 45)
    University = models.CharField(max_length = 70)
    ProjectTopic = models.CharField(max_length = 45)
    EssayTopic = models.CharField(max_length = 45)
    Essay = models.TextField(max_length = 45)
    Picture = models.ImageField(upload_to = 'profilepicture') #size limit to 2000*2000
    HowYouFoundUs = models.CharField(max_length = 100)
    VisaSupportLetterRequired = models.BooleanField(default = False)
    FinancialAidApply = models.BooleanField(default = False) #Applied/NotApplied



class Participant(models.Model):
    ApplicationNo = models.AutoField(primary_key=True)
    ProjectTeamNo = models.PositiveSmallIntegerField()
    AccommodationID = models.IntegerField()
    PaymentStatus = models.CharField(max_length = 45) #Paid/NotPaid/LessPaid/OverPaid
    RequiredPayment = models.IntegerField()
    BreakfastOption = models.BooleanField(default = False)
    DietaryOption = models.CharField(max_length = 45) #Vegetarian/Halal/Others
    PreTour = models.CharField(max_length = 45)
    PostTour = models.CharField(max_length = 45)
    Discount = models.CharField(max_length = 45)


class Accommodation(models.Model):
    AccommodationID = models.IntegerField()
    HotelName = models.CharField(max_length = 45)
    HotelRoom = models.CharField(max_length = 45)
    AccommodationPayment = models.IntegerField()
    Gender = models.CharField(max_length = 45)
    Availability = models.IntegerField()

    
class Discount(models.Model):
    DiscountCode = models.CharField(max_length = 10)
    DiscountValue = models.IntegerField()
    DiscountPercent = models.FloatField()

