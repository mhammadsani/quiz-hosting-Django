from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import QuizAttempter


def host_required(view_function):
    def check_host(request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_superuser:
                try:
                    is_quiz_attempter = QuizAttempter.objects.get(id=request.user.id).is_quiz_attempter
                    if not is_quiz_attempter:
                        return view_function(request, *args, **kwargs)
                except QuizAttempter.DoesNotExist:
                    return view_function(request, *args, **kwargs)
            return render(request, 'error_page.html')
        return HttpResponseRedirect('/login/')
    return check_host


def admin_required(view_function):
    def check_admin(request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return view_function(request)
            return render(request, 'error_page.html')
        return HttpResponseRedirect('/login/')
    return check_admin
