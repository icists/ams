from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.http import HttpResponse
from icists.apps.session.models import UserProfile

# Create your views here.
def get_username(email):
    user = User.objects.filter(email=email)
    if len(user) > 0:
        return user[0].username
    return ''

def login(request):
    if request.user.is_authenticated():
        return redirect('/')

    if request.method == 'POST':
        email = request.POST.get('email', 'none')
        password = request.POST.get('password', 'asdf')
        nexturl = request.POST.get('next', '/')
        
        username = get_username(email)
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect(nexturl)
        else:
            return render(request, 'session/login.html', {'next': nexturl, 'msg': 'Invalid Account Info'})
    return render(request, 'session/login.html', {'next': request.GET.get('next', '/')})


def logout(request):
    if not request.user.is_authenticated():
        return redirect('/')

    auth.logout(request)
    return render(request, 'session/logout.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        birthday = request.POST.get('birthday', '')
        nationality = request.POST.get('nationality', '')
        gender = request.POST.get('gender', '')
        major = request.POST.get('major', '')
        university = request.POST.get('university', '')
        phone = request.POST.get('phone', '')
        # picture = request.POST.get('picture', '')
        how_you_found_us = request.POST.get('howyoufoundus', '')
        
        username = make_password(email)[:20]
        user = User.objects.create_user(username=username, first_name=first_name,
                last_name=last_name, email=email, password=password)

        user_profile = UserProfile(user=user, birthday=birthday, nationality=nationality,
                gender=gender, major=major, university=university, phone=phone,
                how_you_found_us=how_you_found_us)
        user_profile.save()
        return redirect('/')

    return render(request, 'session/signup.html')


def main(request):
    return HttpResponse('Hello, Session!')
