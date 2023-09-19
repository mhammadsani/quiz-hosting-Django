from django.shortcuts import render

def quiz_attempter_homepage(request):
    return render(request, 'quiz_attempter_management/profile.html')
