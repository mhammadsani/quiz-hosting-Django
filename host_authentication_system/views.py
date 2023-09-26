from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from quiz_management.models import QuizAttempter, Quiz, Announcement
from .forms import HostSignUpForm


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
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
           username = form.cleaned_data['username']
           password = form.cleaned_data['password']
           user = authenticate(username=username, password=password)
           if user:
                login(request, user=user)
                try:
                    if temp_user:=QuizAttempter.objects.get(username=username):
                        if temp_user.is_first_time_login:
                            return redirect('/changepassword/')
                        if temp_user.is_quiz_attempter:
                            return redirect('/profile/')
                except Exception as err:
                    return HttpResponseRedirect('/profile/')
    else:       
        form = AuthenticationForm()
    return render(request, 'host_auth_system/login.html', {'form': form})


def waitpage(request):
    return render(request, 'host_auth_system/wait.html')


def profile(request):
    if request.user.is_authenticated:
        try:
            user=QuizAttempter.objects.get(username=request.user.username)
            if user.is_quiz_attempter:
                is_quiz_attempter = True
        except Exception:
            is_quiz_attempter = False
        return render(request, 'host_auth_system/profile.html', {'user': request.user, 'is_quiz_attempter': is_quiz_attempter})   
    return HttpResponseRedirect('/')


def host_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def change_password(request):
    if request.method == "POST":
        updated_credentials = SetPasswordForm(user=request.user, data=request.POST)
        if updated_credentials.is_valid():
            updated_credentials.save()
            try:
                user = QuizAttempter.objects.get(username=request.user.username)
                if user.is_quiz_attempter:
                    user.is_first_time_login = False
                    user.save()
            except Exception as e:
                return HttpResponseRedirect('/quiz_attempter_homepage/')
            return HttpResponseRedirect('/profile/')
        else:
            change_password_form = updated_credentials
    else:
        change_password_form = SetPasswordForm(user=request.user)
    return render(request, 'host_auth_system/change_password.html' ,{'change_password_form':change_password_form})
