from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.http import HttpResponse
from icists.apps.session.models import UserProfile
from icists.apps.session.forms import UserForm, UserProfileForm

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
    if request.user.is_authenticated():
        return redirect('/')

    if request.method == 'POST':
        user_f = UserForm(request.POST)
        user_profile_f = UserProfileForm(request.POST, request.FILES)

        if user_f.is_valid() and user_profile_f.is_valid():
            email = user_f.cleaned_data['email']
            password = user_f.cleaned_data['password']
            first_name = user_f.cleaned_data['first_name']
            last_name = user_f.cleaned_data['last_name']
            birthday = user_profile_f.cleaned_data['birthday']
            nationality = user_profile_f.cleaned_data['nationality']
            gender = user_profile_f.cleaned_data['gender']
            major = user_profile_f.cleaned_data['major']
            university = user_profile_f.cleaned_data['university']
            phone = user_profile_f.cleaned_data['phone']
            picture = user_profile_f.cleaned_data['picture']
            how_you_found_us = user_profile_f.cleaned_data['how_you_found_us']
        
            username = make_password(email)[-21:-1]
            user = User.objects.create_user(username=username, first_name=first_name,
                last_name=last_name, email=email, password=password)
            user.save()

            user_profile = UserProfile(user=user, birthday=birthday, nationality=nationality,
                gender=gender, major=major, university=university, phone=phone, picture=picture,
                how_you_found_us=how_you_found_us)
            user_profile.save()
        return redirect('/')

    return render(request, 'session/signup.html')


def main(request):
    return HttpResponse('Hello, Session!')
