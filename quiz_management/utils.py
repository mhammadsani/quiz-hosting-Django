import json
import pandas as pd
from .models import QuizAttempter, Quiz, Question, User
from .constants import (
                ANSWER, BOOLEAN, EMAIL, EMAILS, IS_PUBLIC, MARKS, MCQS, OPTION_1, OPTION_2, OPTION_3,
                OPTION_4, PASSWORD, QUESTION_TITLE, SUBJECTIVE, TITLE, TYPE
                )


def generate_password():
    password = PASSWORD
    return password


def generate_username(email):
    email = email.split('@')
    return email[0]


def get_emails_from_excel_file(excel_file):
    data_frame = pd.read_excel(excel_file)
    emails = []
    for email in data_frame[EMAILS]:
        emails.append(email)
    return emails


def add_quiz_attempter_by_email(quiz_id, quiz_attempter_form):
    email = quiz_attempter_form.cleaned_data[EMAIL]
    if email:
        username = generate_username(email)
        add_quiz_attempter_to_database(email, username, quiz_id)
    
    
def add_quiz_attempter_by_emails(quiz_id, emails):
    for email in emails:
        username = generate_username(email)
        add_quiz_attempter_to_database(email, username, quiz_id)


def add_quiz_attempter_to_database(email, username, quiz_id):
    try:
        quiz_attempter = QuizAttempter.objects.get(username=username)
        if quiz_attempter:
            quiz = Quiz.objects.get(pk=quiz_id)
            quiz_attempter.quiz_id.add(quiz)
    except Exception as err:
        password = generate_password()
        quiz = Quiz.objects.get(pk=quiz_id)
        quiz_attempter = QuizAttempter.objects.create(username=username, email=email)
        quiz_attempter.quiz_id.add(quiz)
        quiz_attempter.set_password(password)
        quiz_attempter.save()                


def mcq_question(question_form):
    question_title = question_form.cleaned_data[TITLE]
    option1 = question_form.cleaned_data[OPTION_1]
    option2 = question_form.cleaned_data[OPTION_2]
    option3 = question_form.cleaned_data[OPTION_3]
    option4 = question_form.cleaned_data[OPTION_4]
    answer = question_form.cleaned_data[ANSWER]
    is_public = question_form.cleaned_data[IS_PUBLIC]
    marks = question_form.cleaned_data[MARKS]
    question_details = {
        'question_title': question_title,
        'answers': [
            {'option1': option1, 'is_correct_answer': 'option1' == answer },
            {'option2': option2, 'is_correct_answer': 'option2' == answer },
            {'option3': option3, 'is_correct_answer': 'option3' == answer },
            {'option4': option4, 'is_correct_answer': 'option4' == answer },
            ],
        'type': 'mcq'
        }
    return json.dumps(question_details), marks, is_public


def subjective_question(question_form):
    question_title = question_form.cleaned_data[TITLE]
    answer = question_form.cleaned_data[ANSWER]
    marks = question_form.cleaned_data[MARKS]
    is_public = question_form.cleaned_data[IS_PUBLIC]
    question_details = {
        'question_title': question_title, 
        'answers': answer,
        'type': 'subjective'
    }
    return json.dumps(question_details), marks, is_public


def boolean_question(question_form):
    question_title = question_form.cleaned_data[TITLE]
    answer = question_form.cleaned_data[ANSWER]
    marks = question_form.cleaned_data[MARKS]
    is_public = question_form.cleaned_data[IS_PUBLIC]
    question_details = {
        'question_title': question_title, 
        'answers': answer,
        'type': 'boolean'
    }
    return json.dumps(question_details), marks, is_public


def add_question(question_form, quiz_id, type):
    if type == MCQS:
        question_details, marks, is_public = mcq_question(question_form)
    elif type == SUBJECTIVE:
        question_details, marks, is_public = subjective_question(question_form)
    elif type == BOOLEAN:
        question_details, marks, is_public = boolean_question(question_form)
        
    quiz = Quiz.objects.get(pk=quiz_id)
    question = Question.objects.create(question_details=question_details, marks=marks, is_public=is_public)
    question.quiz.add(quiz)
    question.save()
    
def get_final_questions(questions):
    final_questions = []
    for question in questions:
            question_details = json.loads(question.question_details)
            question_title = question_details[QUESTION_TITLE]
            answers = question_details['answers']
            type = question_details[TYPE]
            final_questions.append({
                'question_title': question_title,
                'type': type,
                'answers': answers,
                'id': question.id, 
                'marks': question.marks
            })
    return final_questions


def approve_host(in_active_hosts):
    all_hosts = User.objects.all()
    for host in all_hosts:
        if host.username in in_active_hosts:
            host.is_active = True
            host.save()
            
            
def check_if_quiz_attempted():
    from django.utils import timezone
    current_time = timezone.now()
    quizzes = Quiz.objects.all()
    for quiz in quizzes:
        if current_time >= quiz.start_time and current_time <= quiz.end_time:
            pass
        else:
            quiz.is_quiz_attempted = True
            quiz.save()
            