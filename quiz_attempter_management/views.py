import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.models import User
from .forms import DiscussionForm, CommentForm
from quiz_management.models import Question, QuizAttempter, Announcement, Quiz, QuizAndQuizAttempter
from quiz_attempter_management.models import Answer, Mark, Discussion, Comment


def quiz_attempter_homepage(request):
    return render(request, 'quiz_attempter_management/profile.html')


def show_quizzes(request):
    quiz_attempter = QuizAttempter.objects.get(id=request.user.id)
    quizzes = quiz_attempter.quiz_id.all()
    return render(request, 'quiz_attempter_management/show_quizzes.html', {'quizzes': quizzes})


def show_announcements(request, quiz_id):
    announcements = Announcement.objects.filter(quiz=quiz_id)
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


def save_marks(quiz_attempter, quiz_id, quiz):
    answers = Answer.objects.filter(Q(quiz_attempter=quiz_attempter) & Q(quiz = quiz))
    marks = 0
    total_marks = 0
    for answer in answers:
        user_answer = answer.answer
        question = Question.objects.get(pk=answer.question.id)
        question_details = json.loads(question.question_details)
        total_marks += question.marks
        if question_details["type"] == "mcq":
            options = question_details["answers"]
            print(options, type(options))
            for option_number, option in enumerate(options):
                key = f'option{option_number+1}'
                if option[key] == user_answer and option['is_correct_answer']:
                    marks += question.marks           
        elif question_details['type'] == "subjective":
            if user_answer == question_details["answers"]:
                marks += question.marks

    quiz_attempter = QuizAttempter.objects.get(pk=quiz_attempter)
    quiz = quiz_attempter.quiz_id.get(id=quiz_id)
    mark = Mark(quiz_attempter=quiz_attempter, marks=marks, quiz=quiz, total_mark=total_marks)
    mark.save()


def is_quiz_attemptted(user, quiz_id):
    return QuizAndQuizAttempter.objects.get(Q(quiz_attempter=user) & Q(quiz=quiz_id)).is_attempted


def attempt_quiz(request, quiz_id):
    is_quiz_attempter_by_user = is_quiz_attemptted(request.user, quiz_id)
    if is_quiz_attempter_by_user:
        return redirect(f'/quiz_attempter_homepage/marks/{quiz_id}/')
    final_questions = []
    if request.method == "POST":
        questions = Question.objects.filter(quiz=quiz_id)
        quiz_attempter=QuizAttempter.objects.get(id=request.user.id)
        quiz = Quiz.objects.get(id=quiz_id)
        for question in questions:
            answer = request.POST.get(str(question.id))
            print(answer)
            user_answer = Answer(answer=answer, question=Question.objects.get(id=question.id), quiz_attempter=quiz_attempter, quiz=quiz)
            user_answer.save()
        test=QuizAndQuizAttempter.objects.get(Q(quiz_attempter=request.user) & Q(quiz=quiz_id))
        test.is_attempted = True
        test.save()
        print("I am test ", test)
        save_marks(quiz_attempter, quiz_id, quiz)
        return HttpResponse("Quiz Attempted")
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


def marks(request, quiz_id):
    marks = Mark.objects.filter(quiz_id=quiz_id)
    obtained_marks = 0
    total_marks = 0
    for quiz_attempter in marks:
        print("Request.user.id",request.user.id)
        print("Quiz attempter",quiz_attempter.quiz_attempter.id)
        if quiz_attempter.quiz_attempter.id == request.user.id:
            marks = Mark.objects.get(quiz_attempter=request.user.id)
            obtained_marks = marks.marks
            total_marks = marks.total_mark
    return render(request, 'quiz_attempter_management/marks.html', {'obtained_marks': obtained_marks, 'total_marks': total_marks, 'quiz_id': quiz_id})
