from celery import task

from django.conf import settings
from django.core.mail import send_mail


@task
def task_send_mail(email_title, email_body, email_from, email_to):
    """
    Proceed the email sending task
    """
    send_mail(email_title, email_body, email_from, email_to)
