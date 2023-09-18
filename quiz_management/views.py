import json
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import QuizForm, QuizAttempterForm, MCQsQuestionForm
from .models import QuizAttempter, Quiz, Question


def quiz_management_homepage(request):
    if request.user.is_authenticated:
        return render(request, 'quiz_management/quiz_management.html')
    return HttpResponseRedirect('/')

# def add_quiz_attempter(request):
#     if request.method == "POST":
#         quiz_attempter_form = QuizAttempterForm(request.POST)
#         if quiz_attempter_form.is_valid():
#             email = quiz_attempter_form.cleaned_data['email']
#             password = get_random_password()
#             host = request.user
#             quiz_attempter = QuizAttempter(host=host, email=email, password=password)
#             quiz_attempter.save()
            
#     quiz_attempter_form = QuizAttempterForm()
#     return render(request, 'quiz_management/add_quiz_attempter.html', {'quiz_attmpter': quiz_attempter_form})

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
                quiz.save()
                quiz_form = quiz_form
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
            print('working')
            host.is_active = True
            host.save()
    


def host_management(request):
    if request.user.is_authenticated and request.user.username == 'admin':
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
            ]
        }
    return question_details, marks, is_public


def queston(request, quiz_id, type):
    if request.method == "POST":
        if type == "mcq":
            question_form = MCQsQuestionForm(request.POST)
            if question_form.is_valid():
                question_details, marks, is_public = mcq_question(question_form)
                question_details_json = json.dumps(question_details)
                quiz = Quiz.objects.get(pk=quiz_id)
                question = Question.objects.create(question_details=question_details_json, marks=marks, is_public=is_public)
                question.quiz.add(quiz)
                question.save()
                return HttpResponseRedirect('/quiz_management/question/1/mcq/')
            
            return render(request, 'quiz_management/add_question.html', {'question_form': question_form, 
                                                                 'question_type': "mcqs",
                                                                 })
        
    else:      
        if type == "mcq":
            question_form = MCQsQuestionForm()
            question_type = "mcqs"
            print("working")
        elif type == "subjective":
            question_form = "This is Subjective"
        else:
            question_form = "This is Binary Choice"
        
        return render(request, 'quiz_management/add_question.html', {'question_form': question_form, 
                                                                 'question_type': question_type
                                                                 })
