from django.db import models
from quiz_management.models import QuizAttempter, Quiz, Question


class Answer(models.Model):
    answer = models.CharField(max_length=120)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz_attempter = models.ForeignKey(QuizAttempter, on_delete=models.CASCADE)