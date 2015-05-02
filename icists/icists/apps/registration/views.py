from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from icists.apps.session.models import UserProfile
from icists.apps.registration.models import Application
from icists.apps.registration.forms import ApplicationForm

# Create your views here.


def main(request): # write/edit/view_results for ICISTS-KAIST 2015
    if not request.user.is_authenticated():
        return redirect('/session/login/')

    if Application.objects.filter(user=request.user).exists():
        print "app exists!"
        app = Application.objects.get(user=request.user)
        if app.submit_status:
            print "submitted! pending results."
            return render(request, 'registration/status.html')
        else :
            print "can edit the draft."
            return render(request, 'registration/main.html')
    else:
        #print "app does not exist!" write new.
        return render(request, 'registration/main.html')

def form(request):
    if request.method == "GET":
        return render(request, 'registration/form.html')
    elif request.method == "POST":
        app_f = ApplicationForm(request.POST)

        if app_f.is_valid():
            project_topic = app_f.cleaned_data['project_topic']
            essay_topic = app_f.cleaned_data['essay_topic']
            essay_text = app_f.cleaned_data['essay_text']
            visa_letter_required = app_f.cleaned_data['visa_letter_required']
            financial_aid = app_f.cleaned_data['financial_aid']
            user = request.user

            app = Application(project_topic=project_topic, essay_topic=essay_topic, essay_text=essay_text, visa_letter_required=visa_letter_required, financial_aid=financial_aid, user=user)
            if Application.objects.filter(user=request.user).exists():
                Application.objects.get(user=request.user).delete()
                app.save()
        return redirect('/registration/')
