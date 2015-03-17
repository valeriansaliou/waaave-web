from request_mock import request_mock

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template import RequestContext

from _commons.helpers.mail import send_mail


def comment_email(request, user, target_user, comment, url_full):
    """
    Generate the comment notification email
    """
    content_go_url = '%s#comment-%s' % (request.build_absolute_uri(url_full), comment.id,)

    email_title = '%s %s commented' % (user.first_name, user.last_name,)
    email_from = '%s <%s>' % (settings.EMAIL_NAME, settings.EMAIL_NOREPLY)
    email_to = target_user.email

    email_body = get_template('notification/notification_item_comment_email.jade').render(RequestContext(request, ({
        'comment_user': user,
        'comment_data': comment,
        'content_go_url': content_go_url,
    })))

    send_mail(email_title, email_body, email_from, [email_to])


def response_email(request, user, target_user, comment, url_full):
    """
    Generate the comment response notification email
    """
    content_go_url = '%s#comment-%s' % (request.build_absolute_uri(url_full), comment.id,)

    email_title = '%s %s replied your comment' % (user.first_name, user.last_name,)
    email_from = '%s <%s>' % (settings.EMAIL_NAME, settings.EMAIL_NOREPLY)
    email_to = target_user.email

    email_body = get_template('notification/notification_item_response_email.jade').render(RequestContext(request, ({
        'response_user': user,
        'response_data': comment,
        'content_go_url': content_go_url,
    })))

    send_mail(email_title, email_body, email_from, [email_to])


def spot_email(user, spot, item_type, item_title, item_url):
    """
    Generate the user follow add notification email
    """
    content_go_url = item_url

    title_rep = 'New content added to %s'

    if item_type == 'tutorial':
        title_rep = 'New tutorial added to %s'
    elif item_type == 'book':
        title_rep = 'New book added to %s'

    email_title = title_rep % spot.name
    email_from = '%s <%s>' % (settings.EMAIL_NAME, settings.EMAIL_NOREPLY)
    email_to = user.email

    request = request_mock()

    email_body = get_template('notification/notification_item_spot_email.jade').render(RequestContext(request, ({
        'spot_tag': spot,
        'spot_data': {
            'type': item_type,
            'title': item_title,
        },
        'content_go_url': content_go_url,
    })))

    send_mail(email_title, email_body, email_from, [email_to])


def follow_email(request, user):
    """
    Generate the user follow notification email
    """
    content_go_url = request.build_absolute_uri(reverse('user.views.main', kwargs={
        'username': request.user.username,
    }))

    email_title = '%s %s is following you' % (request.user.first_name, request.user.last_name,)
    email_from = '%s <%s>' % (settings.EMAIL_NAME, settings.EMAIL_NOREPLY)
    email_to = user.email

    email_body = get_template('notification/notification_item_follow_email.jade').render(RequestContext(request, ({
        'follow_user': request.user,
        'content_go_url': content_go_url,
    })))

    send_mail(email_title, email_body, email_from, [email_to])


def follow_add_email(request, user, item_type, item_title, url_full):
    """
    Generate the user follow add notification email
    """
    content_go_url = request.build_absolute_uri(url_full)

    title_rep = '%s %s added new content'

    if item_type == 'tutorial':
        title_rep = '%s %s published a new tutorial'

    email_title = title_rep % (request.user.first_name, request.user.last_name,)
    email_from = '%s <%s>' % (settings.EMAIL_NAME, settings.EMAIL_NOREPLY)
    email_to = user.email

    email_body = get_template('notification/notification_item_follow_add_email.jade').render(RequestContext(request, ({
        'follow_add_user': request.user,
        'follow_add_data': {
            'type': item_type,
            'title': item_title,
        },
        'content_go_url': content_go_url,
    })))

    send_mail(email_title, email_body, email_from, [email_to])
