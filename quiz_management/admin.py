from django.contrib import admin
from .models import Quiz, QuizAttempter, Question, Announcement


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'host', 'title', 'category', 'start_time', 'end_time', 'is_quiz_attempted']


@admin.register(QuizAttempter)
class QuizAttempterAdmin(admin.ModelAdmin):
    list_display = ['username', 'password']
    

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_details', 'is_public', 'marks']
    
    # class Question(models.Model):
    # quiz = models.ManyToManyField(Quiz)
    # question = models.JSONField()
    # is_public = models.BooleanField(default=False)
    # question_marks = models.IntegerField(default=1)

@admin.register(Announcement)
class AnnoucementAdmin(admin.ModelAdmin):
    list_display = ['host', 'quiz', 'subject', 'details']