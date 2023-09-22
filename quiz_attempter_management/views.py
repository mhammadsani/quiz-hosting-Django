import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import DiscussionForm, CommentForm
from quiz_management.models import Question, QuizAttempter, Announcement, Quiz
from quiz_attempter_management.models import Answer, Mark, Discussion, Comment


def quiz_attempter_homepage(request):
    return render(request, 'quiz_attempter_management/profile.html')


def show_quizzes(request):
    quiz_attempter = QuizAttempter.objects.get(id=request.user.id)
    quizzes = quiz_attempter.quiz_id.all()
    return render(request, 'quiz_attempter_management/show_quizzes.html', {'quizzes': quizzes})


def show_announcements(request, quiz_id):
    announcements = Announcement.objects.filter(quiz=quiz_id)
    for announcement in announcements:
        print(announcement.subject)
        print(announcement.details)
    return render(request, 'quiz_attempter_management/announcements.html', {'announcements': announcements})


def discussion_details(request, quiz_id):
    return render(request, 'quiz_attempter_management/discussion.html', {'quiz_id': quiz_id})


def start_discussion(request, quiz_id):
    if request.method == "POST":
        discussion_form = DiscussionForm(request.POST)
        if discussion_form.is_valid():
            subject = discussion_form.cleaned_data['subject']
            details = discussion_form.cleaned_data['details']
            quiz_attempter = QuizAttempter.objects.get(pk=request.user.id)
            quiz = Quiz.objects.get(id=quiz_id)
            discussion = Discussion(subject=subject, details=details, quiz_attempter=quiz_attempter, quiz=quiz)
            discussion.save()
            discussion_form = DiscussionForm()
    else:
        discussion_form = DiscussionForm()
    return render(request, 'quiz_attempter_management/start_discussion.html' , {'discussion_form': discussion_form,
                                                                                'quiz_id': quiz_id})


def view_discussions(request, quiz_id):
    discussions = Discussion.objects.filter(quiz=quiz_id)
    
    return render(request, 'quiz_attempter_management/view_discussion.html', {"discussions": discussions, 
                                                                              'quiz_id': quiz_id})


def full_discussion(request, discussion_id):
    discussion = Discussion.objects.get(id=discussion_id)
    quiz_id = discussion.quiz.id
    print(quiz_id)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.cleaned_data['comment']
            user = User.objects.get(username=request.user.username)
            comment = Comment(comment=user_comment, discussion=discussion, commenter=user)
            comment.save()
            comment_form = CommentForm()

    quizAttempter = QuizAttempter.objects.get(id=discussion.quiz_attempter.id)
    comments = Comment.objects.filter(discussion=discussion)
    comment_form = CommentForm()
    return render(request, 'quiz_attempter_management/full_discussion.html', {'discussion': discussion, 'comments': comments, 'author': quizAttempter.username, 'comment_form': comment_form,
                                                                              'quiz_id': quiz_id})

def save_marks(quiz_attempter):
    answers = Answer.objects.filter(quiz_attempter=quiz_attempter)
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

    quiz_attempter = QuizAttempter.objects.get(pk=quiz_attempter)
    quizzes = quiz_attempter.quiz_id.get()
    print(quizzes)
    
    mark = Mark(quiz_attempter=quiz_attempter, marks=mcq_marks, quiz=quiz)
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
