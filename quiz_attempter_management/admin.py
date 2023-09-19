from django.contrib import admin
from .models import Answer


# Register your models here.
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['quiz_attempter', 'answer', 'question']