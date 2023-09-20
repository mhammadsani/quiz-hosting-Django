from django.db import models
from django.contrib.auth.models import User, AbstractUser


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
    
    
class QuizAttempter(User):
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    is_quiz_attempter = models.BooleanField(default=True, null=True)
    
    def __str__(self) -> str:
        return "Quiz Attempter " + str(self.id)
    
class Announcement(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    details = models.TextField()
    # preparation_material = models.FileField(blank=True)
    