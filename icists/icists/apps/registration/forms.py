from django import forms
from icists.apps.registration.models import Application, Survey


class ApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ApplicationForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['group_name'].required = False

    class Meta:
        model = Application
        fields = ('group_name', 'project_topic', 'essay_topic', 'essay_text',
                  'visa_letter_required', 'financial_aid',
                  'previously_participated')


class FaForm(forms.ModelForm):
    address = forms.CharField(max_length=200)

    class Meta:
        model = Survey
        fields = ('q1', 'q2')
