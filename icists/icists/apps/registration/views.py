from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.exceptions import ValidationError, PermissionDenied, \
    SuspiciousOperation, ObjectDoesNotExist
from django.http import Http404, HttpResponse
from icists.apps.session.models import UserProfile
from icists.apps.registration.models import Application, Survey, ProjectTopic, \
    EssayTopic, Participant, Accommodation
from icists.apps.registration.forms import ApplicationForm, FaForm
import json

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
            except ObjectDoesNotExist:
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
                       'project_topic_2nd': project_topic,
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
    userprofile = UserProfile.objects.get(user=user)

    if request.method == "GET":
        print "GET method. opened the financial."

        return render(request, 'registration/financial.html',
                      {'userprofile': userprofile, 'survey': fa_survey})

    elif request.method == "POST":
        print "POST method; to save the data on financial."
        fa_f = FaForm(data=request.POST, instance=fa_survey)

        try:
            fa_survey = fa_f.save()
            userprofile.address = request.POST.get('address', '')
            userprofile.save()
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


def participation(request):
    print request.method
    if request.method == "GET":
        try:
            assert Application.objects.filter(user=request.user).exists()
            application = Application.objects.get(user=request.user)
            if application.application_category == 'E':
                category = 'Early'
            elif application.application_category == 'R':
                category = 'Regular'
            payment_krw, payment_usd = 0, 0
            if category == 'Early':
                payment_krw = 100000
                payment_usd = 95
            elif category == 'Regular':
                payment_krw = 120000
                payment_usd = 115
            return render(request, 'registration/participation.html',
                          {'category': category,
                           'krw': payment_krw, 'usd': payment_usd})
        except:
            return render(request, 'registration/participation.html',
                          {'error', 'Application data not found'})
    elif request.method == "POST":
        error = []
        print request.POST
        try:
            if 'dietary' in request.POST:
                dietary = request.POST['dietary']
            else:
                error.append('Dietary information missing')
            # print 'dietary', dietary
            if 'accommodation' in request.POST\
                    and int(request.POST['accommodation']) != 0:
                accommodation = int(request.POST['accommodation'])
            else:
                error.append('Please select Accommodation')
            # print 'accommodation', accommodation
            if 'payment' in request.POST\
                    and int(request.POST['payment']) != 0:
                payment = int(request.POST['payment'])
                if payment == 1:
                    payment = 'P'
                    remitter = ''
                if payment == 2:    # Bank Account
                    payment = 'B'
                    if 'remitter' in request.POST\
                            and len(request.POST['remitter']) > 0:
                        remitter = request.POST['remitter']
                    else:
                        remitter = ''
                        error.append('Please indicate Remitter\'s Name for your transaction')
                    # print 'remitter', remitter
            else:
                error.append('Please select Payment Method')
            if 'breakfast' in request.POST:
                breakfast = request.POST['breakfast'] == 'True'
            else:
                error.append('Please choose whether to have Breakfast')
            # print 'breakfast', breakfast
            if 'pretour' in request.POST:
                pretour = request.POST['pretour'] == 'True'
            else:
                error.append('Please choose whether to attend Pre-Conference Banquet')
            # print 'pre', pretour
            if 'posttour' in request.POST:
                posttour = request.POST['posttour'] == 'True'
            else:
                error.append('Please choose whether to attend Post-Conference Banquet')
            print 'arguments processed'
            # print 'post', posttour
            if len(error) > 0:
                return HttpResponse(json.dumps({'success': False,
                                                'error': error}),
                                    content_type='application/json')
            else:
                # calculate total payment
                krw, usd = 0, 0
                application = Application.objects.get(user=request.user)
                if application.application_category == 'E':
                    krw = 100000
                    usd = 95
                elif application.application_category == 'R':
                    krw = 120000
                    usd = 115
                if accommodation == 1:
                    krw += 135000
                    usd += 125
                elif accommodation == 2:
                    krw += 180000
                    usd += 165
                elif accommodation == 3:
                    krw += 120000
                    usd += 110
                elif accommodation == 4:
                    krw += 112500
                    usd += 105
                if breakfast:
                    krw += 20000
                    usd += 20
                if pretour:
                    krw += 40000
                    usd += 30
                if posttour:
                    krw += 100000
                    usd += 90
                print krw, usd

                if Participant.objects.filter(application).exists():
                    print 'paricipant exists, modofication'
                    p = Participant.objects.get(application=application)
                else:
                    p = Participant()
                p.accommodation_choice = accommodation
                p.payment_option = payment
                p.remitter_name = remitter
                p.breakfast_option = breakfast
                p.dietary_option = dietary
                p.pretour = pretour
                p.posttour = posttour
                p.required_payment_krw = krw
                p.required_payment_usd = usd
                p.application = application
                p.submit_time = None
                p.project_team_no = -1
                p.save()
                return HttpResponse(json.dumps({'success': True}),
                                    content_type='application/json')
        except:
            print 'exception', error
            return HttpResponse(json.dumps({'success': False,
                                            'error': error}),
                                content_type='application/json')
