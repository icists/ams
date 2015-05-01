from django import forms 

class ApplicationForm(forms.Form):
    project_topic = forms.CharField(max_length=45)
    essay_topic = forms.TextField(max_length=200)
    essay = forms.TextField()
    visa_support_letter_required = forms.BooleanField(default=False)
    financial_aid_apply = forms.BooleanField(default=False)


