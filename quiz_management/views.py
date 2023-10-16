import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError                    
from quiz_attempter_management.models import Mark
from .constants import (
    ADD_QUESTION_PAGE, ADD_QUESTION_URL, ADD_QUIZ_ATTEMPTER, ADD_QUIZ_ATTEMPTER_URL, ADD_QUIZ_PAGE,
    ADD_QUIZ_SUCCESS_MESSAGE, ANNOUNCEMENT_DONE_MSG, ANNOUNCEMENT_PAGE, APPROVE_HOST, BOOLEAN,
    BOOLEAN_QUESTION_ADDED_SUCCESSFULLY_MSG, BROWSE_QUESTION_URL, CAGTEGORY, DETAILS, DRAFT_QUIZZES_PAGE,
    EDIT_DRAFT, END_TIME, HOST_MANAGEMENT_PAGE, MCQS, MCQS_ADDED_SUCCESSFULLY_MSG, POST, PUBLIC_QUESTION_ADDED_MSG,
    PUBLIC_QUESTIONS_PAGE, QUESTION_TITLE, QUIZ_DRAFT_PAGE, QUIZ_MANAGEMENT_HOMEPAGE, REPORT_PAGE, START_TIME,
    STUDENT_EMAIL_FILE, SUBJECT, SUBJECTIVE, SUBJECTIVE_QUESTION_ADDED_SUCCESSFULLY_MSG, TITLE, TYPE,
)
from .decorators import host_required, admin_required
from .forms import QuizForm, QuizAttempterForm, MCQsQuestionForm, SubjectiveQuestionForm, AnnouncementForm, BooleanQuestionForm
from .models import  Quiz, Question, Announcement, QuizAndQuizAttempter, QuizAttempter
from .utils import (
    get_emails_from_excel_file, add_quiz_attempter_by_email, add_quiz_attempter_by_emails, 
    add_question, get_final_questions, approve_host, check_if_quiz_attempted
)


@host_required
def quiz_management_homepage(request):
    return render(request, QUIZ_MANAGEMENT_HOMEPAGE)


@host_required
def add_quiz(request):
    if request.method == POST:
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            title = quiz_form.cleaned_data[TITLE]
            category = quiz_form.cleaned_data[CAGTEGORY]
            start_time = quiz_form.cleaned_data[START_TIME]
            end_time = quiz_form.cleaned_data[END_TIME]
            quiz = Quiz(
                host=request.user, title=title, category=category, start_time=start_time, end_time=end_time
                )
            quiz.save()
            messages.success(request, ADD_QUIZ_SUCCESS_MESSAGE)
            quiz_form = QuizForm()
            
    else:       
        quiz_form = QuizForm()
    return render(request, ADD_QUIZ_PAGE, {'quiz_form': quiz_form})


@host_required
def draft_quizzes(request):
    quizzes = Quiz.objects.all()
    host = request.user
    current_time = timezone.now()
    attempted_quizzes = []
    unattempted_quizzed = []
    for quiz in quizzes:
        if current_time >= quiz.start_time:
            attempted_quizzes.append(quiz)
        else:
            unattempted_quizzed.append(quiz)
    return render(request, DRAFT_QUIZZES_PAGE, {'quizzes': quizzes, 'attempted_quizzes': attempted_quizzes,
                                                'host': host, 
                                                'unattempted_quizzes': unattempted_quizzed})
    

@admin_required
def host_management(request):
    if request.method == POST:
        in_active_hosts = request.POST.getlist(APPROVE_HOST)
        approve_host(in_active_hosts)

    hosts = User.objects.all()
    return render(request, HOST_MANAGEMENT_PAGE, {'hosts': hosts})
    
   
@host_required 
def add_questions(request, quiz_id):
    return render(request, ADD_QUESTION_PAGE, {'quiz_id': quiz_id})


@host_required
def delete_question(request, quiz_id, question_id):
    quesiton = Question.objects.get(id=question_id)
    quesiton.delete()
    return HttpResponseRedirect(f'{EDIT_DRAFT}/{quiz_id}/')


@host_required
def open_draft(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    current_quiz_questions = []
    for question in questions:
        question_details = json.loads(question.question_details)
        current_quiz_questions.append(
            {
            "title": question_details[QUESTION_TITLE],
            "type": question_details[TYPE],
            'id': question.id
            })
    return render(request, QUIZ_DRAFT_PAGE, {'quiz': quiz, 'questions': current_quiz_questions})
    
    
@host_required
def queston(request, quiz_id, type):
    if request.method == POST:
        if type == MCQS:
            question_form = MCQsQuestionForm(request.POST)
            if question_form.is_valid():
                add_question(question_form, quiz_id, type)
                messages.success(request, MCQS_ADDED_SUCCESSFULLY_MSG)
                return HttpResponseRedirect(f'{ADD_QUESTION_URL}/{quiz_id}/{MCQS}/')
            
            return render(request, ADD_QUESTION_PAGE, {'question_form': question_form, 
                                                                        'question_type': type,
                                                                        'quiz_id': quiz_id
                                                                        })  
        elif type == SUBJECTIVE:
            question_form = SubjectiveQuestionForm(request.POST)
            if question_form.is_valid():
                add_question(question_form, quiz_id, type)
                messages.success(request, SUBJECTIVE_QUESTION_ADDED_SUCCESSFULLY_MSG)
                return HttpResponseRedirect(f'{ADD_QUESTION_URL}/{quiz_id}/{SUBJECTIVE}/')
            
            return render(request, ADD_QUESTION_PAGE, {'question_form': question_form, 
                                                                        'question_type': type,
                                                                        'quiz_id': quiz_id
                                                                        })  
         
        elif type == BOOLEAN:
            question_form = BooleanQuestionForm(request.POST)
            if question_form.is_valid():
                add_question(question_form, quiz_id, type)
                messages.success(request, BOOLEAN_QUESTION_ADDED_SUCCESSFULLY_MSG)
                return HttpResponseRedirect(f'{ADD_QUESTION_URL}/{quiz_id}/{BOOLEAN}/')
            
            return render(request, ADD_QUESTION_PAGE, {'question_form': question_form, 
                                                                        'question_type': type,
                                                                        'quiz_id': quiz_id
                                                                        })  
    else:      
        if type == MCQS:
            question_form = MCQsQuestionForm()
        elif type == SUBJECTIVE:
            question_form = SubjectiveQuestionForm()
        elif type == BOOLEAN:
            question_form = BooleanQuestionForm()
        return render(request, ADD_QUESTION_PAGE, {'question_form': question_form, 
                                                                 'question_type': type,
                                                                 'quiz_id': quiz_id
                                                                 })


@host_required
def add_quiz_attempter(request, quiz_id):
    if request.method == POST:
        quiz_attempter_form = QuizAttempterForm(request.POST)
        if quiz_attempter_form.is_valid():
            try:
                file = request.FILES[STUDENT_EMAIL_FILE]
                if file:
                    emails = get_emails_from_excel_file(file)
                    add_quiz_attempter_by_emails(quiz_id, emails)
            except MultiValueDictKeyError:
                pass
            add_quiz_attempter_by_email(quiz_id, quiz_attempter_form)
            quiz_attempter_form = QuizAttempterForm()
            
    else:       
        quiz_attempter_form = QuizAttempterForm()
    quiz_attempters = QuizAndQuizAttempter.objects.filter(quiz=quiz_id)
    return render(request, ADD_QUIZ_ATTEMPTER, {'quiz_attempter_form': quiz_attempter_form,
                                                                       'quiz_attempters': quiz_attempters, 
                                                                       'quiz_id': quiz_id
    
                                                                   })


@host_required
def delete_quiz_attempter(request, quiz_attempter_id, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    quiz_attempter = QuizAttempter.objects.get(id=quiz_attempter_id)
    quiz_attempter = QuizAndQuizAttempter.objects.get(Q(quiz=quiz) & Q(quiz_attempter=quiz_attempter))
    quiz_attempter.delete()
    return HttpResponseRedirect(f'{ADD_QUIZ_ATTEMPTER_URL}/{quiz_id}/')

    
@host_required
def add_announcement(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    if request.method == POST:
        announcement_form = AnnouncementForm(request.POST)
        if announcement_form.is_valid():
            subject = announcement_form.cleaned_data[SUBJECT]
            details = announcement_form.cleaned_data[DETAILS]
            announcement = Announcement(host=request.user, quiz=quiz, subject=subject, details=details)
            announcement.save()
            announcement_form = AnnouncementForm()
            messages.success(request, ANNOUNCEMENT_DONE_MSG)
    else:
        announcement_form = AnnouncementForm()
    previous_announcements = Announcement.objects.filter(quiz=quiz)
    return render(request, ANNOUNCEMENT_PAGE, {'announcement_form': announcement_form, 
                                                'previous_announcements': previous_announcements,
                                                'quiz_id': quiz_id
                                            })


@host_required
def generate_report(request, quiz_id):
    check_if_quiz_attempted()
    quiz = Quiz.objects.get(id=quiz_id)
    marks = Mark.objects.filter(quiz_id=quiz_id)
    quiz_attempters = QuizAndQuizAttempter.objects.filter(quiz=quiz_id)
    non_attempters = []
    for quiz_attempter in quiz_attempters:    
        if not quiz_attempter.is_attempted:
            non_attempters.append(
                quiz_attempter.quiz_attempter.username
            )
    
    return render(request, REPORT_PAGE, {'marks': marks, 'non_attempters': non_attempters,
                                        'is_quiz_attempted': quiz.is_quiz_attempted,
                                        'quiz_title': quiz.title
                                    })



@host_required
def add_pubilc_question(request, quiz_id, question_id):
    question = Question.objects.get(id=question_id)
    quiz = Quiz.objects.get(id=quiz_id)
    question.quiz.add(quiz)
    question.save()
    messages.success(request, PUBLIC_QUESTION_ADDED_MSG)
    return HttpResponseRedirect(f'{BROWSE_QUESTION_URL}/{quiz_id}/')


@host_required
def browse_public_questions(request, quiz_id):
    questions = Question.objects.all()
    public_questions = [question for question in questions if question.is_public]
    public_questions = get_final_questions(public_questions)
    return render(request, PUBLIC_QUESTIONS_PAGE, {'public_questions': public_questions, 
                                                    'quiz_id': quiz_id
                                                    })
