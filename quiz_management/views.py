import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from quiz_attempter_management.models import Mark
from .decorators import host_required, admin_required
from .forms import QuizForm, QuizAttempterForm, MCQsQuestionForm, SubjectiveQuestionForm, AnnouncementForm
from .models import QuizAttempter, Quiz, Question, Announcement, QuizAndQuizAttempter
from .utils import generate_password, generate_username


@host_required
def quiz_management_homepage(request):
    return render(request, 'quiz_management/quiz_management.html')


@host_required
def add_quiz(request):
    if request.method == "POST":
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            title = quiz_form.cleaned_data['title']
            category = quiz_form.cleaned_data['category']
            start_time = quiz_form.cleaned_data['start_time']
            end_time = quiz_form.cleaned_data['end_time']
            quiz = Quiz(
                host=request.user, title=title, category=category, start_time=start_time, end_time=end_time
                )
            quiz.save()
            messages.success(request, "Quiz Added Successfully")
            quiz_form = QuizForm()
            
    else:       
        quiz_form = QuizForm()
    return render(request, 'quiz_management/add_quiz.html', {'quiz_form': quiz_form})


@host_required
def draft_quizzes(request):
    quizzes = Quiz.objects.all()
    host = request.user
    return render(request, 'quiz_management/draft_quizzes.html', {'quizzes': quizzes, 'host': host})


def approve_host(in_active_hosts):
    all_hosts = User.objects.all()
    for host in all_hosts:
        if host.username in in_active_hosts:
            host.is_active = True
            host.save()
    

@admin_required
def host_management(request):
    if request.method == "POST":
        in_active_hosts = request.POST.getlist('hosts_to_approve')
        approve_host(in_active_hosts)

    hosts = User.objects.all()
    return render(request, 'quiz_management/host_management.html', {'hosts': hosts})
    
   
@host_required 
def add_questions(request, quiz_id):
    return render(request, 'quiz_management/add_question.html', {'quiz_id': quiz_id})


@host_required
def open_draft(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quiz_management/quiz_draft.html', {'quiz': quiz, 
                                                               'questions': questions})


def mcq_question(question_form):
    question_title = question_form.cleaned_data['title']
    option1 = question_form.cleaned_data['option_1']
    option2 = question_form.cleaned_data['option_2']
    option3 = question_form.cleaned_data['option_3']
    option4 = question_form.cleaned_data['option_4']
    answer = question_form.cleaned_data['answer']
    is_public = question_form.cleaned_data['is_public']
    marks = question_form.cleaned_data['marks']
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
    question_title = question_form.cleaned_data['title']
    answer = question_form.cleaned_data['answer']
    marks = question_form.cleaned_data['marks']
    is_public = question_form.cleaned_data['is_public']
    question_details = {
        'question_title': question_title, 
        'answers': answer,
        'type': 'subjective'
    }
    return json.dumps(question_details), marks, is_public


@host_required
def queston(request, quiz_id, type):
    if request.method == "POST":
        if type == "mcq":
            question_form = MCQsQuestionForm(request.POST)
            if question_form.is_valid():
                question_details, marks, is_public = mcq_question(question_form)
                quiz = Quiz.objects.get(pk=quiz_id)
                question = Question.objects.create(question_details=question_details, marks=marks, is_public=is_public)
                question.quiz.add(quiz)
                question.save()
                messages.success(request, "MCQ added successfully!")
                return HttpResponseRedirect(f'/quiz_management/question/{quiz_id}/mcq/')
            
            return render(request, 'quiz_management/add_question.html', {'question_form': question_form, 
                                                                        'question_type': type,
                                                                        })  
        elif type == "subjective":
            question_form = SubjectiveQuestionForm(request.POST)
            if question_form.is_valid():
                question_details, marks, is_public = subjective_question(question_form)
                quiz = Quiz.objects.get(pk=quiz_id)
                question = Question.objects.create(question_details=question_details, marks=marks, is_public=is_public)
                question.quiz.add(quiz)
                question.save()
                messages.success(request, "Subjective Question Added Successfully!")
                return HttpResponseRedirect(f'/quiz_management/question/{quiz_id}/subjective/')
            
            return render(request, 'quiz_management/add_question.html', {'question_form': question_form, 
                                                                        'question_type': type,
                                                                        })  
         
    else:      
        if type == "mcq":
            question_form = MCQsQuestionForm()
        elif type == "subjective":
            question_form = SubjectiveQuestionForm()
        else:
            question_form = "This is Binary Choice"
        
        return render(request, 'quiz_management/add_question.html', {'question_form': question_form, 
                                                                 'question_type': type
                                                                 })



def get_emails_from_excel_file(excel_file):
    import pandas as pd
    data_frame = pd.read_excel(excel_file)
    emails = []
    for email in data_frame['emails']:
        emails.append(email)
    return emails


def add_quiz_attempter_by_email(quiz_id, quiz_attempter_form):
    email = quiz_attempter_form.cleaned_data['email']
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


@host_required
def add_quiz_attempter(request, quiz_id):
    if request.method == "POST":
        quiz_attempter_form = QuizAttempterForm(request.POST)
        if quiz_attempter_form.is_valid():
            try:
                file = request.FILES['students_emails_file']
                if file:
                    emails = get_emails_from_excel_file(file)
                    add_quiz_attempter_by_emails(quiz_id, emails)
            except Exception as err:
                print('following exception has occured', err)
            add_quiz_attempter_by_email(quiz_id, quiz_attempter_form)
            quiz_attempter_form = QuizAttempterForm()
            
    else:       
        quiz_attempter_form = QuizAttempterForm()
    quiz_attempters = QuizAndQuizAttempter.objects.filter(quiz=quiz_id)
        
    print(quiz_attempters)
    return render(request, 'quiz_management/add_quiz_attempter.html', {'quiz_attempter_form': quiz_attempter_form,
                                                                       'quiz_attempters': quiz_attempters
                                                                       })
    
@host_required
def add_announcement(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    if request.method == "POST":
        announcement_form = AnnouncementForm(request.POST)
        if announcement_form.is_valid():
            subject = announcement_form.cleaned_data['subject']
            details = announcement_form.cleaned_data['details']
            # preparation_meterial = announcement_form.cleaned_data['preparation_material']
            announcement = Announcement(host=request.user, quiz=quiz, subject=subject, details=details)
            announcement.save()
            announcement_form = AnnouncementForm()
            messages.success(request, "Announcement Done")
    else:
        announcement_form = AnnouncementForm()
    previous_announcements = Announcement.objects.filter(quiz=quiz)
    return render(request, 'quiz_management/announcement.html', {'announcement_form': announcement_form, 
                                                                 'previous_announcements': previous_announcements
                                                                 })

@host_required
def generate_report(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    marks = Mark.objects.filter(quiz_id=quiz_id)
    quiz_attempters = QuizAndQuizAttempter.objects.filter(quiz=quiz_id)
    non_attempters = []
    for quiz_attempter in quiz_attempters:    
        if not quiz_attempter.is_attempted:
            non_attempters.append(
                quiz_attempter.quiz_attempter.username
            )
    return render(request, 'quiz_management/report.html', {'marks': marks, 'non_attempters': non_attempters,
                                                           'is_quiz_attempted': quiz.is_quiz_attempted,
                                                           'quiz_title': quiz.title})


@host_required
def browse_public_questions(request, quiz_id):
    questions = Question.objects.all()
    public_questions = [question for question in questions if question.is_public]
    return HttpResponse("PUblic Questions")
