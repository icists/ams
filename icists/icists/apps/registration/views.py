from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse('Hello, Registration!')

def status(request): # write/edit/view_results for ICISTS-KAIST 2015
    """
    if :#user has to create a new application form.

    else if :#user has a draft.

    else #user has submitted application.
    """
    return HttpResponse("your application status!")


def form(request):
    if request.method == "GET":
        return render(request, 'registration/form.html')
    elif request.method == "POST":
        app_f = ApplicationForm(request.POST)
        project_topic = app_f.cleaned_data['project_topic']
        essay_topic = app_f.cleaned_data['essay_topic']
        essay_text = app_f.cleaned_data['essay_text']
        visa_letter = app_f.cleaned_data['visa_letter']
        financial_aid = app_f.cleaned_data['financial_aid']

        app = Application(project_topic=project_topic, essay_topic=essay_topic, essay_text=essay_text, visa_letter=visa_letter, financial_aid=financial_aid)
        app.save()
        return redirect('/')
    return render(request, 'registration/form.html')
