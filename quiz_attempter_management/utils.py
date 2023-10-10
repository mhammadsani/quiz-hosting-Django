import json
from quiz_attempter_management.models import Answer, Mark
from django.db.models import Q
from quiz_management.models import (
    Question,
    QuizAttempter,
    QuizAndQuizAttempter,
)
from .constants import (
    ALERT_DANGER, ALERT_SUCCESS, ANSWERS, BOOLEAN, CORRECT_ANSWER,
    MCQS, QUESTION_TITLE, SUBJECTIVE, TYPE
)


def quiz_attempter(user):
    try: 
        user.quizattempter
        return True
    except Exception:
        return False
    
    
def save_marks(quiz_attempter, quiz_id, quiz):
    answers = Answer.objects.filter(Q(quiz_attempter=quiz_attempter) & Q(quiz = quiz))
    marks = 0
    total_marks = 0
    for answer in answers:
        user_answer = answer.answer
        question = Question.objects.get(pk=answer.question.id)
        question_details = json.loads(question.question_details)
        total_marks += question.marks
        if question_details[TYPE] == MCQS:
            options = question_details[ANSWERS]
            for option_number, option in enumerate(options):
                key = f'option{option_number+1}'
                if option[key] == user_answer and option[CORRECT_ANSWER]:
                    marks += question.marks           
        elif question_details[TYPE] == SUBJECTIVE:
            if user_answer == question_details[ANSWERS]:
                marks += question.marks
        elif question_details[TYPE] == BOOLEAN:
            if user_answer == question_details[ANSWERS]:
                marks += question.marks

    quiz_attempter = QuizAttempter.objects.get(pk=quiz_attempter)
    quiz = quiz_attempter.quiz_id.get(id=quiz_id)
    mark = Mark(quiz_attempter=quiz_attempter, marks=marks, quiz=quiz, total_mark=total_marks)
    mark.save()
    
    
def is_quiz_attemptted(user, quiz_id):
    return QuizAndQuizAttempter.objects.get(Q(quiz_attempter=user) & Q(quiz=quiz_id)).is_attempted


def get_final_questions(questions):
    final_questions = []
    for question in questions:
            question_details = json.loads(question.question_details)
            question_title = question_details[QUESTION_TITLE]
            answers = question_details[ANSWERS]
            type = question_details[TYPE]
            final_questions.append({
                'question_title': question_title,
                'type': type,
                'answers': answers,
                'id': question.id
            })
    return final_questions



def get_user_answer_and_correct_answers(answers):
        user_answers_and_correct_answers = []
        for answer in answers:
            question_details = json.loads(answer.question.question_details)
            question_title = question_details[QUESTION_TITLE]
            type = question_details[TYPE]
            if type == MCQS:
                options = question_details[ANSWERS]
                for option in options:
                    if option[CORRECT_ANSWER]:
                        correct_answer = option[list(option.keys())[0]]
                user_answer = answer.answer
                
                alert = ALERT_DANGER
                if user_answer == correct_answer:
                    alert = ALERT_SUCCESS
                
                user_answers_and_correct_answers.append(
                    {
                    'title': question_title,
                    'user_answer': user_answer,
                    'correct_answer': correct_answer,
                    'alert': alert
                    }
                )
                        
            if type == SUBJECTIVE:
                correct_answer = question_details[ANSWERS]
                user_answer = answer.answer
                alert = ALERT_DANGER
                
                if user_answer == correct_answer:
                    alert = ALERT_SUCCESS
                
                user_answers_and_correct_answers.append(
                    {
                    'title': question_title,
                    'user_answer': user_answer,
                    'correct_answer': correct_answer,
                    'alert': alert
                    }
                )
            if type == BOOLEAN:
                correct_answer = question_details[ANSWERS]
                user_answer = answer.answer
                alert = ALERT_DANGER
                if user_answer == correct_answer:
                    alert = ALERT_SUCCESS
                
                user_answers_and_correct_answers.append(
                    {
                    'title': question_title,
                    'user_answer': user_answer,
                    'correct_answer': correct_answer,
                    'alert': alert
                    }
                )
        return user_answers_and_correct_answers
    
    
def get_total_marks(quiz_attempter, quiz):
    answers = Answer.objects.filter(quiz=quiz)
    unique_questions = []
    total_marks = 0
    for answer in answers:
        if answer.question not in unique_questions:
            unique_questions.append(answer.question)
    for question in unique_questions:
        total_marks += question.marks
    return total_marks
