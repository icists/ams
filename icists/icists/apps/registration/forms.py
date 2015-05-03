from django import forms 

class ApplicationForm(forms.Form):
    group_name = forms.CharField(max_length=45)
    project_topic = forms.CharField(max_length=45)
    essay_topic = forms.CharField(max_length=500)
    essay_text = forms.CharField(max_length=5000)
    visa_letter_required = forms.BooleanField()
    financial_aid = forms.BooleanField()


