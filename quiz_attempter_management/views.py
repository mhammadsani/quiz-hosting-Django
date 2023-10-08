import json
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from quiz_management.models import (
    Question,
    QuizAttempter,
    Announcement,
    Quiz,
    QuizAndQuizAttempter,
)
from quiz_attempter_management.models import Answer, Mark, Discussion, Comment
from .forms import DiscussionForm, CommentForm
from .decorators import quiz_attempter_required, host_or_quiz_attempter_required


@quiz_attempter_required
def quiz_attempter_homepage(request):
    return render(request, 'quiz_attempter_management/profile.html')


@quiz_attempter_required
def show_quizzes(request):
    quiz_attempter = QuizAttempter.objects.get(id=request.user.id)
    quizzes = quiz_attempter.quiz_id.all()
    available_quizzes = []
    current_time = timezone.now()
    for quiz in quizzes:
        if current_time >= quiz.start_time and current_time <= quiz.end_time:
            available_quizzes.append(quiz)
        else:
            quiz.is_quiz_attempted = True
            quiz.save()
    return render(request, 'quiz_attempter_management/show_quizzes.html', {'quizzes': quizzes})


@quiz_attempter_required
def show_announcements(request, quiz_id):
    announcements = Announcement.objects.filter(quiz=quiz_id)
    return render(request, 'quiz_attempter_management/announcements.html', {'announcements': announcements})


@quiz_attempter_required
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



@host_or_quiz_attempter_required
def discussion_details(request, quiz_id):
    return render(request, 'quiz_attempter_management/discussion.html', {'quiz_id': quiz_id})


def quiz_attempter(request):
    try: 
        request.user.quizattempter
        is_quiz_attempter = True
    except Exception:
        is_quiz_attempter = False
    return is_quiz_attempter


@host_or_quiz_attempter_required
def view_discussions(request, quiz_id):
    is_quiz_attempter = quiz_attempter(request)
    discussions = Discussion.objects.filter(quiz=quiz_id)
    return render(request, 'quiz_attempter_management/view_discussion.html', {"discussions": discussions, 
                                                                              'quiz_id': quiz_id,
                                                                              'is_quiz_attempter': is_quiz_attempter})


@host_or_quiz_attempter_required
def full_discussion(request, discussion_id):
    discussion = Discussion.objects.get(id=discussion_id)
    quiz_id = discussion.quiz.id
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
    is_quiz_attempter = quiz_attempter(request)
    return render(request, 'quiz_attempter_management/full_discussion.html', {'discussion': discussion, 'comments': comments, 'author': quizAttempter.username, 'comment_form': comment_form,
                                                                              'quiz_id': quiz_id,
                                                                              'is_quiz_attempter': is_quiz_attempter})


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
            for option_number, option in enumerate(options):
                key = f'option{option_number+1}'
                if option[key] == user_answer and option['is_correct_answer']:
                    marks += question.marks           
        elif question_details['type'] == "subjective":
            if user_answer == question_details["answers"]:
                marks += question.marks
        elif question_details['type'] == 'boolean':
            try:
                if user_answer == question_details['answers']:
                    marks += question.marks
            except Exception as err:
                print("Following error has occuered while saving marks", err)

    quiz_attempter = QuizAttempter.objects.get(pk=quiz_attempter)
    quiz = quiz_attempter.quiz_id.get(id=quiz_id)
    mark = Mark(quiz_attempter=quiz_attempter, marks=marks, quiz=quiz, total_mark=total_marks)
    mark.save()


def is_quiz_attemptted(user, quiz_id):
    return QuizAndQuizAttempter.objects.get(Q(quiz_attempter=user) & Q(quiz=quiz_id)).is_attempted


@quiz_attempter_required
def attempt_quiz(request, quiz_id):
    is_quiz_attempter_by_user = is_quiz_attemptted(request.user, quiz_id)
    if is_quiz_attempter_by_user:
        return redirect(f'/quiz-attempter-homepage/marks/{quiz_id}/')
    final_questions = []
    if request.method == "POST":
        questions = Question.objects.filter(quiz=quiz_id)
        quiz_attempter=QuizAttempter.objects.get(id=request.user.id)
        quiz = Quiz.objects.get(id=quiz_id)
        for question in questions:
            answer = request.POST.get(str(question.id))
            user_answer = Answer(answer=answer, question=Question.objects.get(id=question.id), quiz_attempter=quiz_attempter, quiz=quiz)
            user_answer.save()
        test=QuizAndQuizAttempter.objects.get(Q(quiz_attempter=request.user) & Q(quiz=quiz_id))
        test.is_attempted = True
        test.save()
        save_marks(quiz_attempter, quiz_id, quiz)
        return redirect(f'/quiz-attempter-homepage/marks/{quiz_id}/')
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
            quiz_title = Quiz.objects.get(id=quiz_id).title
    return render(request, "quiz_attempter_management/attempt_quiz.html", {'final_questions': final_questions,
                                                                           'quiz_title': quiz_title})


@quiz_attempter_required
def marks(request, quiz_id):
    is_quiz_attemptted = QuizAndQuizAttempter.objects.get(Q(quiz_attempter=request.user) & Q(quiz=quiz_id)).is_attempted
    quiz = Quiz.objects.get(id=quiz_id)
    
    if is_quiz_attemptted:
        marks = Mark.objects.get(Q(quiz_id=quiz_id) & Q(quiz_attempter=request.user.id))
        obtained_marks = marks.marks
        total_marks = marks.total_mark
        answers = Answer.objects.filter(Q(quiz=quiz) & Q(quiz_attempter=request.user.id))
        user_answers_and_correct_answers = []
        for answer in answers:
            question_details = json.loads(answer.question.question_details)
            question_title = question_details['question_title']
            type = question_details['type']
            if type == "mcq":
                options = question_details['answers']
                for option in options:
                    if option['is_correct_answer']:
                        correct_answer = option[list(option.keys())[0]]
                user_answer = answer.answer
                
                alert = "alert alert-danger"
                if user_answer == correct_answer:
                    alert = "alert alert-success"
                
                user_answers_and_correct_answers.append(
                    {
                    'title': question_title,
                    'user_answer': user_answer,
                    'correct_answer': correct_answer,
                    'alert': alert
                    }
                )
                        
            if type == "subjective":
                correct_answer = question_details['answers']
                print(correct_answer)
                
                user_answer = answer.answer
                
                alert = "alert alert-danger"
                if user_answer == correct_answer:
                    alert = "alert alert-success"
                
                user_answers_and_correct_answers.append(
                    {
                    'title': question_title,
                    'user_answer': user_answer,
                    'correct_answer': correct_answer,
                    'alert': alert
                    }
                )
            if type == 'boolean':
                correct_answer = question_details['answers']
                user_answer = answer.answer
                alert = "alert alert-danger"
                if user_answer == correct_answer:
                    alert = "alert alert-success"
                
                user_answers_and_correct_answers.append(
                    {
                    'title': question_title,
                    'user_answer': user_answer,
                    'correct_answer': correct_answer,
                    'alert': alert
                    }
                )
    else:
        return redirect(f'/quiz-attempter-homepage/attempt-quiz/{quiz_id}/')
    return render(request, 'quiz_attempter_management/marks.html', {'obtained_marks': obtained_marks, 'total_marks': total_marks, 'quiz_id': quiz_id, 
                                                                    'user_answers': user_answers_and_correct_answers
                                                                    })
