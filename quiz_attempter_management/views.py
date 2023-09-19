import json
from django.shortcuts import render
from quiz_management.models import Question, QuizAttempter
from quiz_attempter_management.models import Answer


def quiz_attempter_homepage(request):
    return render(request, 'quiz_attempter_management/profile.html')


def attempt_quiz(request, quiz_id):
    final_questions = []
    if request.method == "POST":
        questions = Question.objects.filter(quiz=quiz_id)
        for question in questions:
            answer = request.POST.get(str(question.id))
            user_answer = Answer(answer=answer, question=Question.objects.get(id=question.id), quiz_attempter=QuizAttempter.objects.get(id=request.user.id))
            user_answer.save()
    else:
        questions = Question.objects.filter(quiz=quiz_id)
        # final_questions = []
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