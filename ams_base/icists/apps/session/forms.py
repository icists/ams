from django.forms import ModelForm
from icists.apps.session.models import UserProfile, University
from django.contrib.auth.models import User

class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserProfile
        fields = ('birthday', 'nationality', 'gender', 'phone', 'major', 'university', 'picture', 'how_you_found_us')
