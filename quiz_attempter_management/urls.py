from django.urls import path
from quiz_attempter_management import views

urlpatterns = [
    path('show-quizzes/', views.show_quizzes, name="showquizzes"),
    path("announcements/<int:quiz_id>", views.show_announcements , name="announcements"),
    path('attempt-quiz/<int:quiz_id>/', views.attempt_quiz, name="attemptquiz"),
    path('marks/<int:quiz_id>/', views.marks, name="marks"),
    path('discussion/<int:quiz_id>/', views.discussion_details, name="discussion"),
    path('start-discussion/<int:quiz_id>/', views.start_discussion, name="startdiscussion"),
    path('view-discussions/<int:quiz_id>/', views.view_discussions, name="viewdiscussions"),
    path('full-discussion/<int:discussion_id>/', views.full_discussion, name="fulldiscussion"),
]
