from django.urls import path
from quiz_attempter_management import views

urlpatterns = [
    path('', views.quiz_attempter_homepage, name="quiz_attempter_homepage"),
]
