from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from icists.apps.session.models import UserProfile
from icists.apps.registration.models import Application, Survey
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
            print "can edit the draft." #app_saved.html
            return render(request, 'registration/app_saved.html')
    else:
        #print "app does not exist!" write new. welcome.html
        return render(request, 'registration/welcome.html')

def submit(request):
    if not request.user.is_authenticated():
        return redirect('/session/login/')
    application = Application.objects.get(user=request.user)
    application.submit_status = True
    application.save()
    if application.submit_status:
        print "submitted!"
    else:
        print "not submitted~!"
    return redirect('/registration/')


def form(request):
    if Application.objects.filter(user=request.user).exists():
        print "this is editing"
        application = Application.objects.get(user=request.user)
    else:
        print "this is new app."
        application = Application(user=request.user)

    if request.method == "GET":
        print "it's a get"
        app_f = ApplicationForm(instance=application)
        return render(request, 'registration/form.html', {'application':application, 'user':request.user})

    elif request.method == "POST":
        app_f = ApplicationForm(data=request.POST, instance=application)

        if app_f.is_valid():
            application = app_f.save()

            
            if Survey.objects.filter(application=application).exists():
                survey = Survey.objects.get(application=application)
            else:
                survey = Survey(application=application)
            survey.q1 = app_f.cleaned_data['financial_aid_q1']
            survey.q2 = app_f.cleaned_data['financial_aid_q2']
            survey.save()
            
            print "application saved!!!"

        return redirect('/registration/')
