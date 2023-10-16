from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from quiz_management.models import QuizAttempter
from .constants import (
    CHANGE_PASSWORD_PAGE, CHANGE_PASSWORD_URL, HOMEPAGE_URL, INDEX_PAGE, LOGIN_PAGE, LOGIN_URL,
    PASSWORD, POST, PROFILE_PAGE, PROFILE_URL, SIGN_UP_PAGE, USERNAME, WAIT_PAGE, WAIT_PAGE_URL,
)
from .decorators import is_authenticated
from .forms import HostSignUpForm


def homepage(request):
    return render(request, INDEX_PAGE)


@is_authenticated
def sign_up(request):
    if request.method == POST:
        form = HostSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            return HttpResponseRedirect(WAIT_PAGE_URL)
    else:
        form = HostSignUpForm()
    return render(request, SIGN_UP_PAGE, {'form': form})


@is_authenticated
def user_login(request):
    if request.method == POST:
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
           username = form.cleaned_data[USERNAME]
           password = form.cleaned_data[PASSWORD]
           user = authenticate(username=username, password=password)
           if user:
                login(request, user=user)
                try:
                    if quiz_attempter:=QuizAttempter.objects.get(username=username):
                        if quiz_attempter.is_first_time_login:
                            return redirect(CHANGE_PASSWORD_URL)
                        return redirect(PROFILE_URL)
                except QuizAttempter.DoesNotExist:
                    return HttpResponseRedirect(PROFILE_URL)
    else:       
        form = AuthenticationForm()
    return render(request, LOGIN_PAGE, {'form': form})


def waitpage(request):
    return render(request, WAIT_PAGE)


def profile(request):
    if request.user.is_authenticated:
        try:
            user=QuizAttempter.objects.get(username=request.user.username)
            if user.is_quiz_attempter:
                is_quiz_attempter = True
        except QuizAttempter.DoesNotExist:
            is_quiz_attempter = False
        return render(request, PROFILE_PAGE, {'user': request.user, 'is_quiz_attempter': is_quiz_attempter})   
    return HttpResponseRedirect(HOMEPAGE_URL)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(HOMEPAGE_URL)


def change_password(request):
    if request.method == POST:
        updated_credentials = SetPasswordForm(user=request.user, data=request.POST)
        if updated_credentials.is_valid():
            updated_credentials.save()
            try:
                user = QuizAttempter.objects.get(username=request.user.username)
                if user.is_quiz_attempter:
                    user.is_first_time_login = False
                    user.save()
            except QuizAttempter.DoesNotExist:
                return HttpResponseRedirect(LOGIN_URL)
            return HttpResponseRedirect(PROFILE_URL)
        else:
            change_password_form = updated_credentials
    else:
        change_password_form = SetPasswordForm(user=request.user)
    return render(request, CHANGE_PASSWORD_PAGE ,{'change_password_form':change_password_form})
