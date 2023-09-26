from django.http import HttpResponse
from quiz_management.models import QuizAttempter


def quiz_attempter_required(view_function):
    def check_quiz_attempter(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_superuser:
            try:
                is_quiz_attempter = QuizAttempter.objects.get(id=request.user.id).is_quiz_attempter
                if is_quiz_attempter:
                    return view_function(request, *args, **kwargs)
            except Exception as e:
                return HttpResponse("You are not Quiz Attempter")
    return check_quiz_attempter


def host_or_quiz_attempter_required(view_function):
    def check_host_or_quiz_attempter(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_superuser:
            return view_function(request, *args, **kwargs)
        return HttpResponse("You are not Quiz Attempter or Host")
    return check_host_or_quiz_attempter
