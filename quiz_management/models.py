from django.db import models
from django.contrib.auth.models import User


class QuizAttempter(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(primary_key=True)
    full_name = models.CharField(max_length=120)
    password = models.CharField(max_length=30)


class Quiz(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=30, null=True, blank=True)
    is_quiz_attempted = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    
    def __str__(self) -> str:
        return self.title
    

class Question(models.Model):
    quiz = models.ManyToManyField(Quiz)
    question_details = models.JSONField()
    is_public = models.BooleanField(default=False)
    marks = models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return "Question " + str(self.id)
    
     