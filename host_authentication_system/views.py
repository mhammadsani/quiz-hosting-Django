from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import HostSignUpForm
from quiz_management.models import QuizAttempter


def homepage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile/')
    return render(request, 'host_auth_system/index.html')


def sign_up(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile/')
    if request.method == 'POST':
        form = HostSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            return HttpResponseRedirect('/wait/')
    else:
        form = HostSignUpForm()
    return render(request, 'host_auth_system/sign_up.html', {'form': form})


def user_login(request):
    
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile/')
    if request.method == "POST":
        user_data = AuthenticationForm(request=request, data=request.POST)
        if user_data.is_valid():
           username = user_data.cleaned_data['username']
           password = user_data.cleaned_data['password']
           user = authenticate(username=username, password=password)
           if user:
               login(request, user=user)
            #    user = QuizAttempter.objects.get(username=username)
            #    if user.is_quiz_attempter:
            #        return HttpResponseRedirect('/quiz_attempter_homepage/')
               return HttpResponseRedirect('/profile/')
        form = user_data
    else:       
        form = AuthenticationForm()
    return render(request, 'host_auth_system/login.html', {'form': form})


def waitpage(request):
    return render(request, 'host_auth_system/wait.html')


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'host_auth_system/profile.html', {'user': request.user})
    return HttpResponseRedirect('/')


def host_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def change_password(request):
    if request.method == "POST":
        updated_credentials = PasswordChangeForm(user=request.user, data=request.POST)
        if updated_credentials.is_valid():
            updated_credentials.save()
            return HttpResponseRedirect('/profile/')
        else:
            change_password_form = updated_credentials
    else:
        change_password_form = PasswordChangeForm(user=request.user)
    return render(request, 'host_auth_system/change_password.html' ,{'change_password_form':change_password_form})
