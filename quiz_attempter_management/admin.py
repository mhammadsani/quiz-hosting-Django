from django.contrib import admin
from .models import Answer, Mark, Discussion, Comment


# Register your models here.
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz', 'quiz_attempter', 'answer', 'question']
    
    
@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz_attempter', 'quiz_id', 'marks', 'total_mark']
    

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz_attempter', 'quiz', 'subject', 'details']   


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'discussion', 'comment', 'commenter']
    