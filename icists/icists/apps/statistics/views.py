from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import SuspiciousOperation, PermissionDenied
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.conf import settings
from icists.apps.session.models import UserProfile, University
from icists.apps.session.forms import UserForm, UserProfileForm
from icists.apps.registration.models import Application
import re, os, json, datetime


@staff_member_required
def main(request):
    return render(request, 'statistics/main.html')


@staff_member_required
def get_data(request, query):
    applications = Application.objects.filter(
        submit_time__year = datetime.datetime.now().year
    )
    data = {}
    if query == 'application_category':
        data = {
            'Early': 0,
            'Regular': 0,
            'Late': 0
        }
        verbose = {
            'E': 'Early',
            'R': 'Regular',
            'L': 'Late'
        }
        for app in applications:
            data[verbose[app.application_category]] += 1
    elif query == 'application_status':
        # Not sure what Application Status was.
        pass
    elif query == 'gender':
        data = {
            'Male': 0,
            'Female': 0,
            'Other': 0
        }
        for app in applications:
            userprofile = UserProfile.objects.get(user=app.user)
            if userprofile.gender == 'M':
                data['Male'] += 1
            elif userprofile.gender == 'F':
                data['Female'] += 1
            else:
                data['Other'] += 1
    elif query == 'nationality':
        for app in applications:
            userprofile = UserProfile.objects.get(user=app.user)
            if userprofile.nationality in data:
                data[userprofile.nationality] += 1
            else:
                data[userprofile.nationality] = 1
    elif query == 'university':
        for app in applications:
            userprofile = UserProfile.objects.get(user=app.user)
            if userprofile.university.name in data:
                data[userprofile.university.name] += 1
            else:
                data[userprofile.university.name] = 1
    elif query == 'project_topic':
        for app in applications:
            if str(app.project_topic.number) in data:
                data[str(app.project_topic.number)] += 1
            else:
                data[str(app.project_topic.number)] = 1
    elif query == 'visa':
        data = {
            'Yes': 0,
            'No': 0
        }
        for app in applications:
            if app.visa_letter_required == 'Y':
                data['Yes'] += 1
            else:
                data['No'] += 1
    elif query == 'group_discount':
        data = {
            'Yes': 0,
            'No': 0
        }
        for app in applications:
            if app.group_discount:
                data['Yes'] += 1
            else:
                data['No'] += 1
    elif query == 'how_you_found_us':
        data = {
            '(Not Provided)': 0
        }
        for app in applications:
            userprofile = UserProfile.objects.get(user=app.user)
            if len(userprofile.how_you_found_us) == 0:
                data['(Not Provided)'] += 1
            else:
                if userprofile.how_you_found_us in data:
                    data[userprofile.how_you_found_us] += 1
                else:
                    data[userprofile.how_you_found_us] = 1
    elif query == 'submit_time':
        for app in applications:
            if app.submit_time.strftime("%b %d") in data:
                data[app.submit_time.strftime("%b %d")] += 1
            else:
                data[app.submit_time.strftime("%b %d")] = 1
    # Error in request URL; Generate error
    else:
        return render(request,
                      'statistics/main.html',
                      {'error': 'Error processing statistics query.'})
    # No errors in request URL; Proceed to responding with JSON object
    # return render(request, 'statistic/main.html', json.dumps(data))
    return HttpResponse(json.dumps(data))

'''
@staff_member_required
def change_status(request):
    if request.method == "GET":
        return HttpResponse(json.dumps(
            {'status': settings.APPLICATION_STATUS}))
    if request.is_ajax():
        if request.method == "POST":
            print settings.APPLICATION_STATUS
            try:
                status = request.POST['status']
                print 'status', status
                settings.APPLICATION_STATUS = status
                print settings.APPLICATION_STATUS
                return HttpResponse(json.dumps(
                    {'error': 0}))
            except:
                return HttpResponse(json.dumps(
                    {'error': 1}))
'''
