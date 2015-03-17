from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template import RequestContext

from _commons.helpers.mail import send_mail


def confirm_email(request, key_uidb36, key_token, key_random, email=None):
    """
    Generate the account confirm email
    """
    content_go_url = request.build_absolute_uri(reverse('account.views.confirm_key', args=[key_uidb36,key_token,key_random]))

    email_title = 'Confirm your email address'
    email_from = '%s <%s>' % (settings.EMAIL_NAME, settings.EMAIL_NOREPLY)
    email_to = email or request.user.email

    email_body = get_template('account/account_confirm_email.jade').render(RequestContext(request, ({
        'content_go_url': content_go_url,
    })))

    send_mail(email_title, email_body, email_from, [email_to])


def settings_email_changed_email(request):
    """
    Generate the account email settings changed email
    """
    content_go_url = request.build_absolute_uri(reverse('account.views.settings_root'))

    email_title = 'Email address changed'
    email_from = '%s <%s>' % (settings.EMAIL_NAME, settings.EMAIL_NOREPLY)
    email_to = request.user.email

    email_body = get_template('account/account_settings_email_changed_email.jade').render(RequestContext(request, ({
        'content_go_url': content_go_url,
    })))

    send_mail(email_title, email_body, email_from, [email_to])


def settings_credentials_changed_email(request):
    """
    Generate the account credentials changed email
    """
    content_go_url = request.build_absolute_uri(reverse('account.views.settings_credentials'))

    email_title = 'Password changed'
    email_from = '%s <%s>' % (settings.EMAIL_NAME, settings.EMAIL_NOREPLY)
    email_to = request.user.email

    email_body = get_template('account/account_settings_credentials_changed_email.jade').render(RequestContext(request, ({
        'content_go_url': content_go_url,
    })))

    send_mail(email_title, email_body, email_from, [email_to])


def recover_email(request, email, expire_minutes, key_uidb36, key_token, key_random):
    """
    Generate the account recovery email
    """
    content_go_url = request.build_absolute_uri(reverse('account.views.recover_key', args=[key_uidb36,key_token,key_random]))

    email_title = 'Recover your account password'
    email_from = '%s <%s>' % (settings.EMAIL_NAME, settings.EMAIL_NOREPLY)
    email_to = email

    email_body = get_template('account/account_recover_email.jade').render(RequestContext(request, ({
        'content_go_url': content_go_url,
        'expire_minutes': expire_minutes,
    })))

    send_mail(email_title, email_body, email_from, [email_to])
