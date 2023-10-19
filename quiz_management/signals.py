from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import QuizAttempter, User


def send_username_password(email, username):
    subject = "Be ready for Quiz! "
    message = f'your username is {username} and password is namal123'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
    

@receiver(post_save, sender=QuizAttempter)
def send_email(sender, instance, created, **kwargs):
    if created:
        email = instance.email
        username = instance.username
        send_username_password(email, username)
        
              
@receiver(post_save, sender=User)
def send_email(sender, instance, created, **kwargs):
    if created:
        subject = "New Host Request"
        message = f'There is new person who wants to be host, Verify him!'
        from_email = settings.EMAIL_HOST_USER
        email = instance.email
        recipient_list = [email]
        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
