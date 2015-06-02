from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.exceptions import ValidationError, PermissionDenied, \
    SuspiciousOperation, ObjectDoesNotExist
from icists.apps.session.models import UserProfile
from icists.apps.registration.models import Application, Survey, ProjectTopic, \
    EssayTopic
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


def main(request):  # write/edit/view_results for ICISTS-KAIST 2015
    if not request.user.is_authenticated():
        return redirect('/session/login/')

    if Application.objects.filter(user=request.user).exists():
        print "app exists!"
        app = Application.objects.get(user=request.user)
        if app.submit_time is not None:
            print "submitted! pending results.",\
                app.submit_time, app.screening_result, app.results_embargo
            try:
                return render(request, 'registration/status.html',
                              {'screening': app.screening_result,
                               'embargo': app.results_embargo})
            except app.DoesNotExist:
                return render(request, 'registration/status.html',
                              {'error': 'Object field does not exist'})
        else:
            print "can edit the draft."     # app_saved.html
            # return render(request, 'registration/early_closed.html')
            return render(request, 'registration/draft.html')
    else:
        # print "app does not exist!" write new. welcome.html
        # return render(request, 'registration/early_closed.html')
        return render(request, 'registration/welcome.html')


def submit(request):
    if not request.user.is_authenticated():
        return redirect('/session/login/')
    application = Application.objects.get(user=request.user)
    application.submit_time = timezone.now()
    print 'Application saved at', application.submit_time
    application.save()
    return redirect('/registration/')


def application(request):
    if Application.objects.filter(user=request.user).exists():
        print "Loaded the saved application draft."
        application = Application.objects.get(user=request.user)
    else:
        print "There is no saved application"
        application = Application(user=request.user)

    if request.method == "GET":
        print "GET method. opened the form."
        app_f = ApplicationForm(instance=application)
        project_topic = ProjectTopic.objects.filter(year=2015)\
            .order_by('number')
        essay_topic = EssayTopic.objects.filter(year=2015).order_by('number')
        return render(request, 'registration/application.html',
                      {'application': application,
                       'project_topic': project_topic,
                       'essay_topic': essay_topic})

    elif request.method == "POST":
        print "POST method; to save the data."
        app_f = ApplicationForm(data=request.POST, instance=application)

        try:
            application = app_f.save()
        except:
            print 'Invalid application attempted to save'
            raise ValidationError("app_f is not valid.")

        return redirect('/registration/')


def financial(request):
    if Application.objects.filter(user=request.user).exists():
        print "Loaded the saved application draft."
        application = Application.objects.get(user=request.user)
        if Survey.objects.filter(application=application).exists():
            print "Loaded the saved financial draft."
            fa_survey = Survey.objects.get(application=application)
        else:
            print "There is no saved financial. Hence creating new."
            fa_survey = Survey(application=application)
    else:
        print "There is no saved application"
        redirect('/registration/application')

    user = User.objects.get(username=request.user.username)
    # userprofile = UserProfile.objects.get(user=user)

    if request.method == "GET":
        print "GET method. opened the financial."

        return render(request, 'registration/financial.html',
                      {'user': user, 'survey': fa_survey})

    elif request.method == "POST":
        print "POST method; to save the data on financial."
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
            return render(request, 'registration/cancel.html',
                          {'application': application, 'user': request.user})
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

    return render(request, 'registration/admin_view.html',
                  {'user': user,
                   'userprofile': userprofile,
                   'application': application})


@login_required
def change_status(request, uid=''):
    if request.method != 'POST':
        raise SuspiciousOperation()

    user = process_user_select(request.user, uid)
    application = Application.objects.filter(user=user).first()
    result = request.POST.get('result', 'P')

    if result not in ['P', 'A', 'D']:
        raise SuspiciousOperation()

    application.screening_result = result
    application.save()

    return redirect('/registration/admin-view/' + user.username)


def participant(request):
    return render(request, 'registration/participant.html')
