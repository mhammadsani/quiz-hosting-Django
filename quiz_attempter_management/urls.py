from django.urls import path
from quiz_attempter_management import views

urlpatterns = [
    path('', views.quiz_attempter_homepage, name="quiz_attempter_homepage"),
    path('show_quizzes/', views.show_quizzes, name="showquizzes"),
    path("announcements/<int:quiz_id>", views.show_announcements , name="announcements"),
    path('attempt_quiz/<int:quiz_id>/', views.attempt_quiz, name="attemptquiz"),
    path('marks/', views.marks, name="marks"),
    path('discussion_details/<int:quiz_id>/', views.discussion_details, name="discussion"),
    path('start_discussion/<int:quiz_id>/', views.start_discussion, name="startdiscussion"),
    path('view_discussions/<int:quiz_id>/', views.view_discussions, name="viewdiscussions"),
    path('full_discussion/<int:discussion_id>/', views.full_discussion, name="fulldiscussion")
]
