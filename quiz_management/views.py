import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import QuizForm, QuizAttempterForm, MCQsQuestionForm, SubjectiveQuestionForm, AnnouncementForm
from .models import QuizAttempter, Quiz, Question, Announcement
from .utils import generate_password, generate_username


def quiz_management_homepage(request):
    if request.user.is_authenticated:
        return render(request, 'quiz_management/quiz_management.html')
    return HttpResponseRedirect('/')


def add_quiz(request):
    if request.user.is_authenticated:
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
                print(request.user)
                quiz.save()
                messages.success(request, "Quiz Added Successfully")
                quiz_form = QuizForm()
                
        else:       
            quiz_form = QuizForm()
        return render(request, 'quiz_management/add_quiz.html', {'quiz_form': quiz_form})
    else:
        return HttpResponseRedirect('/')


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
    

def host_management(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == "POST":
            in_active_hosts = request.POST.getlist('hosts_to_approve')
            print('in active hosts are ', in_active_hosts)
            approve_host(in_active_hosts)

        hosts = User.objects.all()
        return render(request, 'quiz_management/host_management.html', {'hosts': hosts})
    else:
        return HttpResponseRedirect('/profile/')
    
    
def add_questions(request, quiz_id):
    return render(request, 'quiz_management/add_question.html', {'quiz_id': quiz_id})


def open_draft(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    for question in questions:
        print(question.question_details)
        print(question.marks)
        print(question.is_public)
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
    print("Following is the Answer ", answer)
    print(question_title, option1, option2, option4, option3, answer, is_public, marks)
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
                return HttpResponseRedirect('/quiz_management/question/1/mcq/')
            
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
                return HttpResponseRedirect('/quiz_management/question/2/subjective/')
            
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



def add_quiz_attempter(request, quiz_id):
    if request.method == "POST":
        quiz_attempter_form = QuizAttempterForm(request.POST)
        if quiz_attempter_form.is_valid():
            email = quiz_attempter_form.cleaned_data['email']
            username = generate_username(email)
            password = generate_password()
            print(username, password)
            quiz = Quiz.objects.get(pk=quiz_id)
            quiz_attempter = QuizAttempter.objects.create(username=username, email=email, quiz_id=quiz)
            quiz_attempter.set_password(password)
            quiz_attempter.save()
            messages.success(request, "Quiz Attempter Added for the quiz")
            quiz_attempter_form = QuizAttempterForm()
    else:       
        quiz_attempter_form = QuizAttempterForm()
    quiz_attempters = QuizAttempter.objects.filter(pk=quiz_id)
    print(quiz_attempters)
    return render(request, 'quiz_management/add_quiz_attempter.html', {'quiz_attempter_form': quiz_attempter_form,
                                                                       'quiz_attempters': quiz_attempters
                                                                       })
    

def add_announcement(request, quiz_id):
    if request.method == "POST":
        announcement_form = AnnouncementForm(request.POST)
        if announcement_form.is_valid():
            subject = announcement_form.cleaned_data['subject']
            details = announcement_form.cleaned_data['details']
            # preparation_meterial = announcement_form.cleaned_data['preparation_material']
            quiz = Quiz.objects.get(pk=quiz_id)
            announcement = Announcement(host=request.user, quiz=quiz, subject=subject, details=details)
            announcement.save()
            announcement_form = AnnouncementForm()
            messages.success(request, "Announcement Done")
    else:
        announcement_form = AnnouncementForm()
    return render(request, 'quiz_management/announcement.html', {'announcement_form': announcement_form})


def generate_report(request):
    pass