from django import forms

class UserForm(forms.Form):
    email = forms.CharField(max_length = 50)
    password = forms.CharField(max_length = 50)
    first_name = forms.CharField(max_length = 30)
    last_name = forms.CharField(max_length = 30)

class UserProfileForm(forms.Form):
    birthday = forms.DateField()
    nationality = forms.CharField(max_length = 45)
    gender = forms.CharField(max_length = 45)
    phone = forms.CharField(max_length = 45)
    major = forms.CharField(max_length = 45)
    university = forms.CharField(max_length = 70)
    picture = forms.ImageField()
    how_you_found_us = forms.CharField(max_length = 100)
