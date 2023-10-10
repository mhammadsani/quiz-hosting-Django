from django.urls import path
from quiz_management import views


urlpatterns = [
    path('', views.quiz_management_homepage,  name="quizmanagement"),
    path('host-management/', views.host_management, name="hostmanagement"),
    path('add-quiz/', views.add_quiz, name="addquiz"),
    path('draft-quizzes/', views.draft_quizzes, name="draftquizzes"),
    path('edit-draft/<int:quiz_id>/', views.open_draft, name="draft"),
    path('add-quiz-attempter/<int:quiz_id>/', views.add_quiz_attempter, name="addquizattempter" ), 
    path('add-announcement/<int:quiz_id>/', views.add_announcement, name="announcement"),
    path('add-question/<int:quiz_id>/', views.add_questions, name='addquestion'),
    path('question/<int:quiz_id>/<str:type>/', views.queston, name="questiontype"),
    path('generate-report/<quiz_id>', views.generate_report, name='generatereport'),
    path('browse-public-questions/<int:quiz_id>/', views.browse_public_questions, name="publicquestions"),
    path('delete-quiz-attempter/<int:quiz_attempter_id>/<int:quiz_id>/', views.delete_quiz_attempter, name="deletequizattempter"),
    path('delete-question/<int:quiz_id>/<int:question_id>/', views.delete_question, name="deletequestion"),
    path('browse-questions/<int:quiz_id>/', views.browse_public_questions, name="browsequestions" ),
    path('add-pubilc-question/<int:quiz_id>/<int:question_id>/', views.add_pubilc_question, name="addpublicquestion")
]
