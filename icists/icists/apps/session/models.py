from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birthday = models.DateField()
    nationality = models.CharField(max_length = 45)
    gender = models.CharField(max_length = 45)
    phone = models.CharField(max_length = 45) #country_code + number
    major = models.CharField(max_length = 45)
    university = models.CharField(max_length = 70)
    picture = models.ImageField(upload_to = 'profilepicture') #size limit to 2000*2000
    how_you_found_us = models.CharField(max_length = 100)
