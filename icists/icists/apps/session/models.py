from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your models here.
def validate_image(image_obj):
    filesize = image_obj.file.size
    if filesize > 2 * 1024 * 1024:
        raise ValidationError("Size of image should less than 2MB")

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birthday = models.DateField()
    nationality = models.CharField(max_length=45)
    gender = models.CharField(max_length=45)
    phone = models.CharField(max_length=45) #country_code + number
    major = models.CharField(max_length=45)
    university = models.CharField(max_length=70)
    picture = models.ImageField(upload_to='profilepicture', null=True, blank=True,
            validators=[validate_image]) #size limit to 2MB
    how_you_found_us = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
