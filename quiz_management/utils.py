from .models import QuizAttempter, Quiz


def generate_password(length=16):
    password = "namal123"
    return password


def generate_username(email):
    email = email.split('@')
    return email[0]


def get_emails_from_excel_file(excel_file):
    import pandas as pd
    data_frame = pd.read_excel(excel_file)
    emails = []
    for email in data_frame['emails']:
        emails.append(email)
    return emails


def add_quiz_attempter_by_email(quiz_id, quiz_attempter_form):
    email = quiz_attempter_form.cleaned_data['email']
    if email:
        username = generate_username(email)
        add_quiz_attempter_to_database(email, username, quiz_id)
    
    
def add_quiz_attempter_by_emails(quiz_id, emails):
    for email in emails:
        username = generate_username(email)
        add_quiz_attempter_to_database(email, username, quiz_id)


def add_quiz_attempter_to_database(email, username, quiz_id):
    try:
        quiz_attempter = QuizAttempter.objects.get(username=username)
        if quiz_attempter:
            quiz = Quiz.objects.get(pk=quiz_id)
            quiz_attempter.quiz_id.add(quiz)
    except Exception as err:
        password = generate_password()
        quiz = Quiz.objects.get(pk=quiz_id)
        quiz_attempter = QuizAttempter.objects.create(username=username, email=email)
        quiz_attempter.quiz_id.add(quiz)
        quiz_attempter.set_password(password)
        quiz_attempter.save()                
