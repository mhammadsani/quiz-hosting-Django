from django.shortcuts import render
from quiz_management.models import Question


def quiz_attempter_homepage(request):
    return render(request, 'quiz_attempter_management/profile.html')


def attempt_quiz(request, quiz_id):
    questions = Question.objects.filter(quiz=quiz_id)
    for question in questions:
        print(question.question_details)
        print(question.marks)
        print(question.is_public)
    return render(request, "quiz_attempter_management/attempt_quiz.html")