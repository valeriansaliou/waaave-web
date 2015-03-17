from _commons.tasks import task_send_mail


def send_mail(email_title, email_body, email_from, email_to):
    task_send_mail.delay(email_title, email_body, email_from, email_to)