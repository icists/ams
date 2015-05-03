from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from icists.apps.session.models import UserProfile
from icists.apps.session.forms import UserProfileForm
from icists.apps.registration.models import Application, Survey
from icists.apps.registration.forms import ApplicationForm

# Create your views here.


def main(request): # write/edit/view_results for ICISTS-KAIST 2015
    if not request.user.is_authenticated():
        return redirect('/session/login/')

    if Application.objects.filter(user=request.user).exists():
        print "app exists!"
        app = Application.objects.get(user=request.user)
        if app.submit_time is not None:
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
    application.submit_time = timezone.now()
    print 'Application saved at', application.submit_time
    application.save()
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
        if Survey.objects.filter(application=application).exists():
            survey = Survey.objects.get(application=application)
        else:
            survey = Survey()

        return render(request, 'registration/form.html', {'application':application, 'user':request.user, 'survey':survey})

    elif request.method == "POST":
        print "it's a post"
        app_f = ApplicationForm(data=request.POST, instance=application)

        user = User.objects.get(username=request.user.username)

        userprofile = UserProfile.objects.get(user=user)

        try:
            application = app_f.save()
        except:
            print 'Invalid application attempted to save'
            raise ValidationError()

        return redirect('/registration/')
