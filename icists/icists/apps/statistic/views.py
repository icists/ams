from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import SuspiciousOperation, PermissionDenied
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from icists.apps.session.models import UserProfile, University
from icists.apps.session.forms import UserForm, UserProfileForm
import re, os, json

# Create your views here.
@staff_member_required
def main(request):
    return render(request, 'statistic/main.html')
    
