from django.urls import path
from quiz_attempter_management import views

urlpatterns = [
    path('', views.quiz_attempter_homepage, name="quiz_attempter_homepage"),
    path('show_quizzes/', views.show_quizzes, name="showquizzes"),
    path("announcements/<int:quiz_id>", views.show_announcements , name="announcements"),
    path('attempt_quiz/<quiz_id>/', views.attempt_quiz, name="attemptquiz"),
    path('marks/', views.marks, name="marks")
]
