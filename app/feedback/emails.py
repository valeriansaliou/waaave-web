from request_mock import request_mock

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template import RequestContext
from django.conf import settings

from _commons.helpers.mail import send_mail


def report_email(request, user, form):
    """
    Generate the feedback report email
    """
    full_name = '%s %s' % (user.first_name, user.last_name)
    email = user.email

    email_title = 'Waaave feedback'
    email_from = '%s <%s>' % (full_name, email)
    email_to = [admin[1] for admin in settings.ADMINS]

    email_body = get_template('feedback/feedback_report_email.jade').render(RequestContext(request, ({
        'full_name': full_name,
        'email': email,
        'form': form,

        'has_go': False,
        'has_footer': False,
    })))

    send_mail(email_title, email_body, email_from, email_to)


def invite_email(user):
    """
    Generate the feedback invite email
    """
    path_reversed = reverse('feedback.views.root')
    request = request_mock(
        path=path_reversed,
        user=user
    )

    content_go_url = request.build_absolute_uri(path_reversed)

    email_title = '%s, we need your feedback!' % user.first_name
    email_from = '%s <%s>' % (settings.EMAIL_NAME, settings.EMAIL_NOREPLY)
    email_to = user.email

    email_body = get_template('feedback/feedback_invite_email.jade').render(RequestContext(request, ({
        'invite_user': user,
        'content_go_url': content_go_url,
    })))

    send_mail(email_title, email_body, email_from, [email_to])
