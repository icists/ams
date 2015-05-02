from django import forms 

class ApplicationForm(forms.Form):
    project_topic = forms.CharField(max_length=45)
    essay_topic = forms.CharField(max_length=500)
    essay_text = forms.CharField(widget = forms.Textarea)
    visa_letter_required = forms.BooleanField()
    financial_aid = forms.BooleanField()


