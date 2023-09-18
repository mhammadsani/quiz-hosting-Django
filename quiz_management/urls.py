from django.urls import path
from quiz_management import views


urlpatterns = [
    path('', views.quiz_management_homepage,  name="quizmanagement"),
    path('host_management/', views.host_management, name="hostmanagement"),
    path('add_quiz/', views.add_quiz, name="addquiz"),
    path('draft_quizzes/', views.draft_quizzes, name="draftquizzes"),
    path('add_question/<int:quiz_id>/', views.add_questions, name='addquestion'),
    path('question/<int:quiz_id>/<str:type>/', views.queston, name="questiontype"),
    path('edit_draft/<int:quiz_id>/', views.open_draft, name="draft")
]
