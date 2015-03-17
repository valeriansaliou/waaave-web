from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse

from honeypot.decorators import check_honeypot

from models import *
from forms import *
from emails import *


def root(request):
    """
    Company > Root
    """
    return HttpResponsePermanentRedirect(
        reverse('company.views.about')
    )


def about(request):
    """
    Company > About
    """
    return render(request, 'company/company_about.jade')


def terms(request):
    """
    Company > Terms
    """
    return render(request, 'company/company_terms.jade')


def privacy(request):
    """
    Company > Privacy
    """
    return render(request, 'company/company_privacy.jade')


@check_honeypot
def contact(request):
    """
    Company > Contact
    """
    user = request.user
    message_sent = False

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            Contact(
                user=(user if user.is_authenticated() else None),
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                reason=form.cleaned_data['reason'],
                message=form.cleaned_data['message']
            ).save()

            contact_email(
                request,
                form.cleaned_data['full_name'],
                form.cleaned_data['email'],
                form.cleaned_data['reason'],
                form.cleaned_data['message']
            )

            message_sent = True
    
    if request.method != 'POST' or message_sent:
        full_name, email = None, None

        if user.is_authenticated():
            full_name = '%s %s' % (user.first_name, user.last_name)
            email = user.email

        form = ContactForm(initial={
            'full_name': full_name,
            'email': email,
            'reason': 'none'
        })

    return render(request, 'company/company_contact.jade', {
        'form': form,
        'message_sent': message_sent
    })
