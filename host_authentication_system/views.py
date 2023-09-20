from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .forms import HostSignUpForm
from quiz_management.models import QuizAttempter, Quiz


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
            #    if user.is_admin:
            #         return redirect('admin_dashboard')
            #    elif user.is_host:
            #         return redirect('host_dashboard')
            #    elif user.is_quiz_attempter:
            #         return redirect('quiz_attempter_dashboard')
                try:
                    if temp_user:=QuizAttempter.objects.get(username=username):
                        quiz = Quiz.objects.get(pk=temp_user.quiz_id.id)
                        if temp_user.is_quiz_attempter:
                            print("QUiz id is ", quiz.id)
                            return render(request, 'quiz_attempter_management/profile.html/', {'quiz': quiz})
                except Exception as err:
                    print("Following exception is occuring ", err)
                    return HttpResponseRedirect('/profile/')
        form = user_data
    else:       
        form = AuthenticationForm()
    return render(request, 'host_auth_system/login.html', {'form': form})


def waitpage(request):
    return render(request, 'host_auth_system/wait.html')


def profile(request):
    if request.user.is_authenticated:
        print("I am the main User", dir(request.user))
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
