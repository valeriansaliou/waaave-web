from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.loader import get_template

from _commons.helpers.mail import send_mail


def tutorial_moderated_email(request, status, moderation_message, author_email, tutorial_id, tut_title, tut_tag, tut_slug):
    """
    Send the tutorial moderated email notification
    """
    assert status == 'accepted' or status == 'refused'

    if status == 'accepted':
        reverse_path = reverse('tutorial.views.view', kwargs={'tag': tut_tag, 'slug': tut_slug})
    elif status == 'refused':
        reverse_path = reverse('dashboard.views.tutorial_edit', kwargs={'tutorial_id': tutorial_id})
    content_go_url = request.build_absolute_uri(reverse_path)

    email_title = 'Your tutorial has been %s' % status
    email_from = '%s <%s>' % (settings.EMAIL_NAME, settings.EMAIL_NOREPLY)
    email_to = author_email

    email_body = get_template('moderation/moderation_tutorial_%s_email.jade' % status).render(RequestContext(request, ({
        'tut_title': tut_title,
        'content_go_url': content_go_url,
        'moderation_message': moderation_message,
    })))

    send_mail(email_title, email_body, email_from, [email_to])