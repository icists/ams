from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.serializers import serialize
from django.http import HttpResponse
from icists.apps.session.models import UserProfile
from icists.apps.registration.models import Application, Survey, ProjectTopic, \
    EssayTopic, Participant
from icists.apps.policy.models import Configuration, Price, PaymentInfo, AccommodationOption
from icists.apps.registration.forms import ApplicationForm, FaForm
# from datetime import datetime
import json
import sys

# Create your views here.


cnf = Configuration.objects.all()[0]
app_stage = cnf.application_stage
price = Price.objects.filter(year=cnf.year).first()
open_stage = {
    'E': Configuration.EARLY,
    'R': Configuration.REGULAR,
    'L': Configuration.LATE,
}
closed_stage = {
    'BE': Configuration.BEFORE_EARLY,
    'EC': Configuration.EARLY_CLOSED,
    'RC': Configuration.REGULAR_CLOSED,
    'LC': Configuration.LATE_CLOSED,
}


@login_required
def main(request):  # write/edit/view_results for ICISTS-KAIST 2015
    if not request.user.is_authenticated():
        return redirect('/session/login/')

    if Application.objects.filter(user=request.user).exists():
        ''' application form exists. Go on with editing. '''
        app = Application.objects.get(user=request.user)

        if app.submit_time is not None:
            ''' application form exists and has been submitted. '''
            if Participant.objects.filter(application=app).exists():
                print 'paricipant exists, modification'
                p = Participant.objects.get(application=app)
            else:
                p = Participant()
            payment_status = p.payment_status

            print "submitted! pending results.",\
                app.submit_time, app.screening_result, app.results_embargo
            try:
                return render(request, 'registration/status.html',
                              {'screening': app.screening_result,
                               'embargo': app.results_embargo,
                               'submitted': False,
                               'payment_status': payment_status,
                               })
            except ObjectDoesNotExist:
                return render(request, 'registration/status.html',
                              {'error': 'Object field does not exist'})
        else:
            '''application form exists, but has not been saved. '''
            print "can edit the draft."
            # return render(request, 'registration/early_closed.html')
            if (app_stage == Configuration.BEFORE_EARLY):
                return render(request, 'registration/app_closed.html')
            else:
                return render(request, 'registration/draft.html')

    else:
        ''' application form does not exist. redirected to welcome page '''
        print "application does not exist."
        if (app_stage in open_stage.values()):
            return render(request, 'registration/welcome.html')
        elif (app_stage in closed_stage.values()):
            return render(request, 'registration/app_closed.html')


@login_required
def submit(request):
    if not request.user.is_authenticated():
        return redirect('/session/login/')
    application = Application.objects.get(user=request.user)
    application.submit_time = timezone.now()
    # application.application_category = settings.APPLICATION_STATUS
    print "app_stage at submission : ", app_stage
    if app_stage in closed_stage.values():
        raise "nothing to be submitted when application_closed."
    application.application_category = app_stage
    print 'Application saved at', application.submit_time
    application.save()
    return redirect('/registration/')


@login_required
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
        project_topic = ProjectTopic.objects.filter(year=cnf.year)\
            .order_by('number')
        essay_topic = EssayTopic.objects.filter(year=cnf.year).order_by('number')
        return render(request, 'registration/app_form.html',
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
            print "Unexpected error:", sys.exc_info()[0]
            raise ValidationError("app_f is not valid.")

        return redirect('/registration/')


@login_required
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


def participation(request):
    print request.method
    # GET : when the user opens the form page.
    if request.method == "GET":
        try:
            assert Application.objects.filter(user=request.user).exists()
            application = Application.objects.get(user=request.user)

            if Participant.objects.filter(application=application).exists():
                print 'Participation object exists'
                p = Participant.objects.get(application=application)
            else:
                print 'Participation object does not exist, \
                    hence create a new object.'
                p = Participant()
                p.application = application

            category_price_krw, category_price_usd = p.payment()
            print 'payment success'

            ao_qs = AccommodationOption.objects.all()
            ao_s = serialize("json", ao_qs)
            print ao_s

            return render(request, 'registration/participation.html',
                          {'participant': p,
                           'category': application.get_application_category_display(),
                           'krw': category_price_krw, 'usd': category_price_usd,
                           'category_price_krw': category_price_krw,
                           'category_price_usd': category_price_usd,
                           'group_discount_bool': application.group_discount,
                           'payment_info': PaymentInfo.objects.first(),
                           'accommodation_options': ao_qs,
                           'ao_s': ao_s
                           })
        except:
            return render(request, 'registration/participation.html',
                          {'error', 'Application data not found'})

    # POST : when the user completed the form and submitted.
    elif request.method == "POST":
        error = []
        print request.POST
        try:
            if 'dietary' in request.POST:
                dietary = request.POST['dietary']
            else:
                error.append('Dietary information missing')

            if 'recommender' in request.POST:
                recommender_name = request.POST['recommender']
            if 'accommodation' in request.POST\
                    and int(request.POST['accommodation']) != 0:
                accommodation_id = int(request.POST['accommodation'])
            else:
                error.append('Please select Accommodation')
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
                        error.append('Please indicate Remitter\'s Name \
                                     for your transaction')
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
                error.append('RSVP for Pre-Conference Program')
            # print 'pre', pretour
            '''
            if 'posttour' in request.POST:
                posttour = request.POST['posttour'] == 'True'
            else:
                error.append('RSVP for Post-Conference Tour')
            '''
            # post tour conference set to false for all application
            posttour = False
            print 'arguments processed'
            # print 'post', posttour
            if len(error) > 0:
                return HttpResponse(json.dumps({'success': False,
                                                'error': error}),
                                    content_type='application/json')
            else:

                app = Application.objects.get(user=request.user)
                if Participant.objects.filter(application=app).exists():
                    print 'paricipant exists, modofication'
                    p = Participant.objects.get(application=app)
                else:
                    p = Participant()
                    p.application = app

                p.accommodation_choice = accommodation_id
                p.accommodation_option = AccommodationOption.objects.get(id=accommodation_id)
                p.payment_option = payment
                p.remitter_name = remitter
                p.breakfast_option = breakfast
                p.dietary_option = dietary
                p.pretour = pretour
                p.posttour = posttour
                p.recommender_name = recommender_name

                # calculate total payment
                krw, usd = p.payment()

                p.required_payment_krw = krw
                p.required_payment_usd = usd
                p.submit_time = None
                p.project_team_no = 0
                p.save()
                return HttpResponse(json.dumps({'success': True}),
                                    content_type='application/json')
        except:
            print 'exception', error
            return HttpResponse(json.dumps({'success': False,
                                            'error': error}),
                                content_type='application/json')
        return redirect('/registration/')
