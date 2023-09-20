import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from quiz_management.models import Question, QuizAttempter, Announcement, Quiz
from quiz_attempter_management.models import Answer, Mark


def quiz_attempter_homepage(request):
    return render(request, 'quiz_attempter_management/profile.html')


def show_quizzes(request):
    quiz = QuizAttempter.objects.get(id=request.user.id).quiz_id
    return render(request, 'quiz_attempter_management/show_quizzes.html', {'quiz': quiz})


def show_announcements(request, quiz_id):
    announcements = Announcement.objects.filter(quiz=quiz_id)
    for announcement in announcements:
        print(announcement.subject)
        print(announcement.details)
    return render(request, 'quiz_attempter_management/announcements.html', {'announcements': announcements})


def save_marks(quiz_attempter):
    answers = Answer.objects.filter(quiz_attempter=quiz_attempter)
    print(answers)
    mcq_marks = 0
    mcq_total_marks = 0
    for answer in answers:
        question = Question.objects.get(pk=answer.question.id)
        user_answer = answer.answer
        question_details = json.loads(question.question_details)
        if question_details["type"] == "mcq":
            options = question_details["answers"]
            for option_number, option in enumerate(options):
                key = f'option{option_number+1}'
                if option[key] == user_answer and option['is_correct_answer']:
                    mcq_marks += question.marks
                    mcq_total_marks += question.marks
    mark = Mark(quiz_attempter=quiz_attempter, marks=mcq_marks, quiz=quiz_attempter.quiz_id)
    mark.save()


def is_quiz_attemptted(user, quiz_id):
    marks = Mark.objects.all()
    for mark in marks:
        if mark.quiz_attempter.id == user and mark.quiz_id == int(quiz_id):
            return True
    return False


def attempt_quiz(request, quiz_id):
    is_quiz_attempter_by_user = is_quiz_attemptted(request.user.id, quiz_id)
    print(is_quiz_attempter_by_user)
    if is_quiz_attempter_by_user:
        return HttpResponse("Quiz is Already Attempted by You")
    final_questions = []
    if request.method == "POST":
        questions = Question.objects.filter(quiz=quiz_id)
        quiz_attempter=QuizAttempter.objects.get(id=request.user.id)
        for question in questions:
            answer = request.POST.get(str(question.id))
            user_answer = Answer(answer=answer, question=Question.objects.get(id=question.id), quiz_attempter=quiz_attempter)
            user_answer.save()
        save_marks(quiz_attempter)
    else:
        questions = Question.objects.filter(quiz=quiz_id)
        for question in questions:
            question_details = json.loads(question.question_details)
            question_title = question_details['question_title']
            answers = question_details['answers']
            type = question_details['type']
            final_questions.append({
                'question_title': question_title,
                'type': type,
                'answers': answers,
                'id': question.id
            })
    return render(request, "quiz_attempter_management/attempt_quiz.html", {'final_questions': final_questions})


def marks(request):
    marks = Mark.objects.get(quiz_attempter=request.user.id).marks
    print(marks)
    return render(request, 'quiz_attempter_management/marks.html', {'mcq_marks': marks})
"""
{"question_title": "What is OS?", "answers": [{"option1": "subject", "is_correct_answer": false}, {"option2": "a way to interact with hardware", "is_correct_answer": false}, {"option3": "operating system", "is_correct_answer": false}, {"option4": "all", "is_correct_answer": true}]}
1
False
"""

"""
{'question_title': 'What is OS?', 'type': 'mcq', 
'answers': [{'option1': 'subject', 'is_correct_answer': False}, 
{'option2': 'core of computer science', 'is_correct_answer': False}, 
{'option3': 'operating system', 'is_correct_answer': False}, 
{'option4': 'all', 'is_correct_answer': True}]}

{'question_title': 'What is OS?', 'type': 'subjective', 
'answers': 'Operating System is a software that helps you communicate with the hardware in an easy manner.'}
"""