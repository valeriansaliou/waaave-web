from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template import RequestContext
from django.conf import settings

from _commons.helpers.mail import send_mail


def contact_email(request, full_name, email, reason, message):
    """
    Generate the contact email
    """
    email_title = 'Waaave contact'
    email_from = '%s <%s>' % (full_name, email)
    email_to = [admin[1] for admin in settings.ADMINS]

    email_body = get_template('company/company_contact_email.jade').render(RequestContext(request, ({
        'full_name': full_name,
        'email': email,
        'reason': reason,
        'message': message,

        'has_go': False,
        'has_footer': False,
    })))

    send_mail(email_title, email_body, email_from, email_to)
