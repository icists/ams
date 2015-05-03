from django import forms
from icists.apps.registration.models import Application

class ApplicationForm(forms.ModelForm):
#    financial_aid_q1 = forms.CharField(max_length=2000)
#    financial_aid_q2 = forms.CharField(max_length=2000)
#    address = forms.CharField(max_length=200)
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ApplicationForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['group_name'].required = False
    class Meta:
        model = Application
        #fields = ('group_name', 'project_topic', 'essay_topic', 'essay_text', 'visa_letter_required', 'financial_aid', 'previously_participated', 'financial_aid_q1', 'financial_aid_q2') 
        fields = ('group_name', 'project_topic', 'essay_topic', 'essay_text', 'visa_letter_required', 'financial_aid', 'previously_participated')

