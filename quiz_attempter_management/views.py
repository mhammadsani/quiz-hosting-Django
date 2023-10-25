from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone
from quiz_management.models import (
    Question, QuizAttempter, Announcement, Quiz, QuizAndQuizAttempter,
)
from quiz_attempter_management.models import Answer, Mark, Discussion, Comment
from .constants import (
    QUIZ_ATTEMPTER_PROFILE_PAGE, QUIZZES_PAGE, ANNOUNCEMENT_PAGE, POST, SUBJECT, DETAILS, 
    START_DISCUSSION_PAGE, DISCUSSION_PAGE, VIEW_DISCUSSION_PAGE, COMMENT, FULL_DISCUSSION_PAGE,
    MARKS_URL, ATTEMPT_QUIZZ_PAGE, MARKS_PAGE, ATTEMPT_QUIZZ_URL
)
from .decorators import is_quiz_attempter, is_host_or_quiz_attempter
from .forms import DiscussionForm, CommentForm
from .utils import (
    check_quiz_attempter, is_quiz_attemptted, save_marks, get_final_questions, 
    get_user_answer_and_correct_answers, get_total_marks
)


@is_quiz_attempter
def quiz_attempter_homepage(request):
    return render(request, QUIZ_ATTEMPTER_PROFILE_PAGE)


@is_quiz_attempter
def show_quizzes(request):
    quiz_attempter = QuizAttempter.objects.get(id=request.user.id)
    quizzes = quiz_attempter.quiz_id.all()
    available_quizzes = []
    attempted_quizzes = []
    quiz_to_be_started_yet = []
    current_time = timezone.now()
    for quiz in quizzes:
        if current_time >= quiz.start_time and current_time <= quiz.end_time:
            available_quizzes.append(quiz)
        elif current_time < quiz.start_time:
            quiz_to_be_started_yet.append(quiz)
        else:
            quiz.is_quiz_attempted = True
            quiz.save()
            attempted_quizzes.append(quiz)
    return render(request, QUIZZES_PAGE, {'available_quizzes': available_quizzes, 
                                        'attempted_quizzes': attempted_quizzes,
                                        'quiz_to_be_started_yet': quiz_to_be_started_yet
                                        })


@is_quiz_attempter
def show_announcements(request, quiz_id):
    announcements = Announcement.objects.filter(quiz=quiz_id)
    return render(request, ANNOUNCEMENT_PAGE, {'announcements': announcements})


@is_quiz_attempter
def start_discussion(request, quiz_id):
    if request.method == POST:
        discussion_form = DiscussionForm(request.POST)
        if discussion_form.is_valid():
            subject = discussion_form.cleaned_data[SUBJECT]
            details = discussion_form.cleaned_data[DETAILS]
            quiz_attempter = QuizAttempter.objects.get(pk=request.user.id)
            quiz = Quiz.objects.get(id=quiz_id)
            discussion = Discussion(subject=subject, details=details, quiz_attempter=quiz_attempter, quiz=quiz)
            discussion.save()
            discussion_form = DiscussionForm()
    else:
        discussion_form = DiscussionForm()
    return render(request, START_DISCUSSION_PAGE , {'discussion_form': discussion_form,
                                                    'quiz_id': quiz_id})


@is_host_or_quiz_attempter
def discussion_details(request, quiz_id):
    return render(request, DISCUSSION_PAGE, {'quiz_id': quiz_id})


@is_host_or_quiz_attempter
def view_discussions(request, quiz_id):
    is_quiz_attempter = check_quiz_attempter(request.user)
    discussions = Discussion.objects.filter(quiz=quiz_id)
    return render(request, VIEW_DISCUSSION_PAGE, {"discussions": discussions, 
                                                'quiz_id': quiz_id,
                                                'is_quiz_attempter': is_quiz_attempter})


@is_host_or_quiz_attempter
def full_discussion(request, discussion_id):
    discussion = Discussion.objects.get(id=discussion_id)
    quiz_id = discussion.quiz.id
    if request.method == POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.cleaned_data[COMMENT]
            user = User.objects.get(username=request.user.username)
            comment = Comment(comment=user_comment, discussion=discussion, commenter=user)
            comment.save()
            comment_form = CommentForm()

    quiz_attempter = QuizAttempter.objects.get(id=discussion.quiz_attempter.id)
    comments = Comment.objects.filter(discussion=discussion)
    comment_form = CommentForm()
    is_quiz_attempter = check_quiz_attempter(request.user)
    return render(request, FULL_DISCUSSION_PAGE, 
                  {'discussion': discussion, 'comments': comments, 
                    'author': quiz_attempter.username,
                    'comment_form': comment_form,
                    'quiz_id': quiz_id,
                    'is_quiz_attempter': is_quiz_attempter
                    }
                  )


@is_quiz_attempter
def attempt_quiz(request, quiz_id):
    is_quiz_attempter_by_user = is_quiz_attemptted(request.user, quiz_id)
    if is_quiz_attempter_by_user:
        return redirect(f'{MARKS_URL}/{quiz_id}/')
    final_questions = []
    if request.method == POST:
        questions = Question.objects.filter(quiz=quiz_id)
        quiz_attempter = QuizAttempter.objects.get(id=request.user.id)
        quiz = Quiz.objects.get(id=quiz_id)
        for question in questions:
            answer = request.POST.get(str(question.id))
            user_answer = Answer(answer=answer, question=Question.objects.get(id=question.id), quiz_attempter=quiz_attempter, quiz=quiz)
            user_answer.save()
        quiz_and_quiz_attempter_instance=QuizAndQuizAttempter.objects.get(Q(quiz_attempter=request.user) & Q(quiz=quiz_id))
        quiz_and_quiz_attempter_instance.is_attempted = True
        quiz_and_quiz_attempter_instance.save()
        save_marks(quiz_attempter, quiz_id, quiz)
        return redirect(f'{MARKS_URL}/{quiz_id}/')
    else:
        questions = Question.objects.filter(quiz=quiz_id)
        final_questions = get_final_questions(questions)
        quiz_title = Quiz.objects.get(id=quiz_id).title
    return render(request, ATTEMPT_QUIZZ_PAGE, {'final_questions': final_questions,
                                                'quiz_title': quiz_title})
    
    
@is_quiz_attempter
def marks(request, quiz_id):
    current_time = timezone.now()
    quiz = Quiz.objects.get(id=quiz_id)
    quiz_attempter = QuizAttempter.objects.get(id=request.user.id)
    is_quiz_attemptted = QuizAndQuizAttempter.objects.get(Q(quiz_attempter=request.user) & Q(quiz=quiz_id)).is_attempted
    if current_time >= quiz.end_time and not is_quiz_attemptted:
        total_marks = get_total_marks(quiz_attempter, quiz)
        marks = Mark(quiz_attempter=quiz_attempter, quiz_id=quiz_id, marks=0, total_mark=total_marks)
        marks.save()
        is_quiz_attemptted = QuizAndQuizAttempter.objects.get(Q(quiz_attempter=request.user) & Q(quiz=quiz_id))
        is_quiz_attemptted.is_attempted = True
        is_quiz_attemptted.save()
    
    if is_quiz_attemptted:
        marks = Mark.objects.get(Q(quiz_id=quiz_id) & Q(quiz_attempter=request.user.id))
        obtained_marks = marks.marks
        total_marks = marks.total_mark
        answers = Answer.objects.filter(Q(quiz=quiz) & Q(quiz_attempter=request.user.id))
        user_answers_and_correct_answers = get_user_answer_and_correct_answers(answers)
        
    else:
        return redirect(f'{ATTEMPT_QUIZZ_URL}/{quiz_id}/')
    return render(request, MARKS_PAGE, {'obtained_marks': obtained_marks, 'total_marks': total_marks, 'quiz_id': quiz_id, 
                                                                    'user_answers': user_answers_and_correct_answers
                                                                    })
