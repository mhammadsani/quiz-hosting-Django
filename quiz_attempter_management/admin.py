from django.contrib import admin
from .models import Answer, Mark


# Register your models here.
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['quiz_attempter', 'answer', 'question']
    
    
@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ['quiz_attempter', 'quiz_id', 'marks']