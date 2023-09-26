from django.urls import path
from quiz_management import views


urlpatterns = [
    path('', views.quiz_management_homepage,  name="quizmanagement"),
    path('host_management/', views.host_management, name="hostmanagement"),
    path('add_quiz/', views.add_quiz, name="addquiz"),
    path('draft_quizzes/', views.draft_quizzes, name="draftquizzes"),
    path('edit_draft/<int:quiz_id>/', views.open_draft, name="draft"),
    path('add_quiz_attempter/<int:quiz_id>/', views.add_quiz_attempter, name="addquizattempter" ), 
    path('add_announcement/<int:quiz_id>/', views.add_announcement, name="announcement"),
    path('add_question/<int:quiz_id>/', views.add_questions, name='addquestion'),
    path('question/<int:quiz_id>/<str:type>/', views.queston, name="questiontype"),
    path('generate_report/<quiz_id>', views.generate_report, name='generatereport'),
    path('browse_public_questions/<int:quiz_id>/', views.browse_public_questions, name="publicquestions")
]
