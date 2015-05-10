from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib.auth.models import User
from icists.apps.session.models import UserProfile
from icists.apps.session.forms import UserProfileForm
from icists.apps.registration.models import Application, Survey
from icists.apps.registration.forms import ApplicationForm, FaForm

# Create your views here.

def process_user_select(cuser, uid=''):
    if not cuser.is_staff:
        raise PermissionDenied()

    if uid == '':
        uid = cuser.username

    userl = User.objects.filter(username=uid)
    if len(userl) < 1:
        raise Http404()
    return userl[0]


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
        print "Loaded the saved application draft."
        application = Application.objects.get(user=request.user)
    else:
        print "There is no saved application"
        application = Application(user=request.user)

    if request.method == "GET":
        print "GET method. opened the form."
        app_f = ApplicationForm(instance=application)
        return render(request, 'registration/form.html', {'application':application})

    elif request.method == "POST":
        print "POST method; to save the data."
        app_f = ApplicationForm(data=request.POST, instance=application)


        try:
            application = app_f.save()
        except:
            print 'Invalid application attempted to save'
            raise ValidationError("app_f is not valid.")

        return redirect('/registration/')


def fa_form(request):
    if Application.objects.filter(user=request.user).exists():
        print "Loaded the saved application draft."
        application = Application.objects.get(user=request.user)
        if Survey.objects.filter(application=application).exists():
            print "Loaded the saved fa_form draft."
            fa_survey = Survey.objects.get(application=application)
        else:
            print "There is no saved fa_form. Hence creating new."
            fa_survey = Survey(application=application)
    else:
        print "There is no saved application"
        redirect('/registration/form')

    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)

    if request.method == "GET":
        print "GET method. opened the fa_form."

        return render(request, 'registration/fa_form.html', {'user':user, 'survey':fa_survey})

    elif request.method == "POST":
        print "POST method; to save the data on fa_form."
        fa_f = FaForm(data=request.POST, instance=fa_survey)

        try:
            fa_survey = fa_f.save()
        except:
            print 'Invalid application attempted to save'
            raise ValidationError()

        return redirect('/registration/')


def cancel(request):
    try:
        application = Application.objects.get(user=request.user)
        if request.method == "GET":
            return render(request, 'registration/cancel.html', {'application':application, 'user': request.user})
        elif request.method == "POST":
            application.delete()
            return redirect('/registration/')
    except Application.DoesNotExist:
        return redirect('/registration/')


@login_required
def admin_view(request, uid=''):
    user = process_user_select(request.user, uid)
    userprofile = UserProfile.objects.get(user=user)
    application = Application.objects.filter(user=user).first()

    return render(request, 'registration/admin_view.html', {'user': user, 'userprofile': userprofile, 'application':application})


@login_required
def change_status(request, uid=''):
    if not request.user.is_staff:
        raise PermissionDenied()
    user = process_select_user(request.user, uid)
