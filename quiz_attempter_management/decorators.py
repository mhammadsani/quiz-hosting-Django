from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from quiz_management.models import QuizAttempter


def is_quiz_attempter(view_function):
    def check_quiz_attempter(request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_superuser:
                try:
                    is_quiz_attempter = QuizAttempter.objects.get(id=request.user.id).is_quiz_attempter
                    if is_quiz_attempter:
                        return view_function(request, *args, **kwargs)
                except QuizAttempter.DoesNotExist:
                    return render(request, 'error_page.html')
        return HttpResponseRedirect('/login/')
    return check_quiz_attempter


def is_host_or_quiz_attempter(view_function):
    def check_host_or_quiz_attempter(request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_superuser:
                return view_function(request, *args, **kwargs)
            return render(request, 'error_page.html')
        return HttpResponseRedirect('/login/')
    return check_host_or_quiz_attempter
