from django.contrib.auth.models import User
from django.db import models
from quiz_management.models import QuizAttempter, Quiz, Question


class Answer(models.Model):
    answer = models.CharField(max_length=120)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz_attempter = models.ForeignKey(QuizAttempter, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    
    
class Mark(models.Model):
    marks = models.IntegerField()
    total_mark = models.IntegerField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    quiz_attempter = models.ForeignKey(QuizAttempter, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-marks']
    

class Discussion(models.Model):
    quiz_attempter = models.ForeignKey(QuizAttempter, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)    
    details = models.TextField()

    
class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    