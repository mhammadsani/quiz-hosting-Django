from django.db.models.signals import post_save
from .models import QuizAttempter
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail


def send_email_to_client(email, username):
    subject = "You have been added to the Following Quiz "
    message = f'your username is {username} and password is namal123'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
    

@receiver(post_save, sender=QuizAttempter)
def send_email(sender, instance, created, **kwargs):
    if created:
        email = instance.email
        username = instance.username
        send_email_to_client(email, username)
    