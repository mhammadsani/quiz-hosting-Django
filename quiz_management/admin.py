from django.contrib import admin
from .models import Quiz, QuizAttempter, Question, Announcement, QuizAndQuizAttempter, QuizAndQuestion


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'host', 'title', 'category', 'start_time', 'end_time', 'is_quiz_attempted']


@admin.register(QuizAttempter)
class QuizAttempterAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'password']
    

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_details', 'is_public', 'marks']


@admin.register(Announcement)
class AnnoucementAdmin(admin.ModelAdmin):
    list_display = ['id', 'host', 'quiz', 'subject', 'details']
    
    
@admin.register(QuizAndQuizAttempter)
class QuizAndQuizAttempterAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz_attempter', 'quiz', 'is_attempted']
    

@admin.register(QuizAndQuestion)
class QuizAndQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz', 'question', 'quiz_attempter', 'answer']