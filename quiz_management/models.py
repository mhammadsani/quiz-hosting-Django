from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Quiz(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=30, null=True, blank=True)
    is_quiz_attempted = models.BooleanField(default=False)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)

 
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['start_time', 'end_time']
    

class Question(models.Model):
    quiz = models.ManyToManyField(Quiz)
    question_details = models.JSONField()
    is_public = models.BooleanField(default=False)
    marks = models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return "Question " + str(self.id)
    

class QuizAttemptersExcel(models.Model):
    file = models.FileField(upload_to='uploads/')    


class QuizAttempter(User):
    quiz_id = models.ManyToManyField(Quiz, through="QuizAndQuizAttempter")
    is_quiz_attempter = models.BooleanField(default=True, null=True)
    is_first_time_login = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return "Quiz Attempter " + str(self.id)
    
    class Meta:
        db_table = "Quiz Attempter"
        
        
class QuizAndQuizAttempter(models.Model):
    quiz_attempter = models.ForeignKey(QuizAttempter, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    is_attempted = models.BooleanField(default=False)
    
    
class Announcement(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    details = models.TextField()
    