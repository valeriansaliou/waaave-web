import json
from datetime import datetime
from time import time
from urllib import unquote
from requests.exceptions import HTTPError, ConnectionError

import social
from social.apps.django_app.views import auth as social_auth
from social.apps.django_app.views import complete as social_complete
from social.apps.django_app.views import disconnect as social_disconnect
from social.exceptions import AuthAlreadyAssociated, AuthCanceled, AuthTokenError,\
                              AuthStateMissing, AuthUnknownError, AuthTokenRevoked,\
                              NotAllowedToDisconnect

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from _commons.decorators.security import anon_required, auth_required, reg_required, new_required
from _commons.forms import defaults
from _commons.helpers.rank import RankHelper
from _commons.shortcuts import get_user
from rank.helpers import RankProcessHelper
from notification.helpers import NotificationHelper
from avatar.helpers import AvatarHelper
from avatar.models import Binding as AvatarBinding

from .forms import *
from .models import *
from .helpers import *
from .emails import *
from .factories import *
from .pipeline import *


# -- Login: Responses --
@anon_required
def login_root(request):
    """
    Account > Login Root
    """
    error_notif = {
        'has': False,
        'short': None,
        'long': None
    }

    login_next = request.GET.get('next', None)

    # Build boolean object from GET parameters
    params = {}
    for param in ('required', 'social_auth_failed', 'social_auth_revoked'):
        params[param] = request.GET.get(param, None) is not None

    # Disable next action for unrelevant pages (logout)
    if login_next == reverse('account.views.logout_root') or login_next == reverse('account.views.login_root'):
        login_next = None

    # Save data?
    if request.method == 'POST':
        form = LoginRootForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember = form.cleaned_data['remember']
            login_username = username

            # Get actual username or email
            user_exists = True
            user = get_user(username=username, email=username)

            if user is not None:
                username = user.username
            else:
                user_exists = False

            if user_exists is True:
                user = authenticate(username=username, password=password)

                if user is not None:
                    if user.is_active:
                        if remember:
                            request.session.set_expiry(settings.SESSION_REMEMBER_EXPIRITY)

                        # Proceed login
                        login(request, user)

                        # Check registration resume state
                        RegisterHelper.update_resume(request)

                        # Any comment to be moved from pool?
                        move_comment_pool(request, user)

                        # Next URL after login is done?
                        if login_next:
                            response = HttpResponseRedirect(login_next)
                        else:
                            response = HttpResponseRedirect(reverse('home.views.root'))

                        # Remember username for next time we login...
                        response.set_cookie('login_username', login_username, max_age=settings.SESSION_REMEMBER_EXPIRITY)

                        return response
                    else:
                        error_notif['has'] = True
                        error_notif['short'] = 'Account suspended.'
                        error_notif['long'] = 'Your account has been suspended.'
                else:
                    error_notif['has'] = True
                    error_notif['short'] = 'Wrong password.'
                    error_notif['long'] = 'We could not log you in. Check your password and retry.'
            else:
                error_notif['has'] = True
                error_notif['short'] = 'Wrong username.'
                error_notif['long'] = 'We could not log you in. Check your username and retry.'
        else:
            error_notif['has'] = True
            error_notif['short'] = 'Missing field.'
            error_notif['long'] = 'Please provide both a valid username and password.'
    else:
        login_username = request.COOKIES.get('login_username', None)
        form = LoginRootForm(initial={'username': login_username})

    return render(request, 'account/account_login.jade', {
        'form': form,
        'error_notif': error_notif,
        'login_next': login_next,
        'has_login_required': params['required'],
        'social_auth_failed': params['social_auth_failed'],
        'social_auth_revoked': params['social_auth_revoked'],
    })


def login_social(request, backend):
    """
    Account > Login Social
    """
    return social_auth(request, backend)


def complete_social(request, backend):
    """
    Account > Complete Social
    """
    try:
        return social_complete(request, backend)
    except AuthAlreadyAssociated:
        return HttpResponseRedirect(settings.SOCIAL_AUTH_CONNECT_ERROR_URL)
    except AuthTokenRevoked:
        return HttpResponseRedirect(settings.SOCIAL_AUTH_LOGIN_REVOKED_URL)
    except (HTTPError, ConnectionError, AuthCanceled, AuthTokenError, AuthStateMissing, AuthUnknownError):
        return HttpResponseRedirect(settings.SOCIAL_AUTH_LOGIN_ERROR_URL)


def disconnect_social(request, backend):
    """
    Account > Disconnect Social
    """
    try:
        return social_disconnect(request, backend)
    except NotAllowedToDisconnect:
        return HttpResponseRedirect(settings.SOCIAL_AUTH_DISCONNECT_ERROR_URL)


# -- Logout: Responses --
def logout_root(request):
    """
    Account > Logout Root
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home.views.root'))

    first_name = request.user.first_name
    logout(request)

    return render(request, 'account/account_logout.jade', {
        'first_name': first_name,
    })


# -- Register: Responses --
@anon_required
def register_root(request):
    """
    Account > Register Root
    """
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('account.views.register_go'))

    return render(request, 'account/account_register_root.jade', {
        'current_step': 'root',
    })


@new_required
def register_go(request):
    """
    Account > Register Go
    """
    has_password = not request.user.is_authenticated()

    # Save data?
    if request.method == 'POST' and request.POST.get('current_step') == 'go':
        form = RegisterGoForm(request.POST, has_password=has_password)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password'] if 'password' in form.cleaned_data else None

            if request.user.is_authenticated():
                user = request.user

                user.email = email
                user.set_password(password)
                
                user.save()
            else:
                # Create user
                user_f = UserFactory()
                user_f.create(email, password)

                user = user_f.get_user()

                # Login user
                user = authenticate(username=user_f.get_user().username, password=password)
                request.session.set_expiry(settings.SESSION_REMEMBER_EXPIRITY)
                login(request, user)

            # Store registration state
            register = Register.objects.get_or_create(
                user=user,
                defaults={
                    'ip_start': request.META['REMOTE_ADDR'],
                    'ip_update': request.META['REMOTE_ADDR'],
                },
            )[0]
            register.step_current = 1
            register.save()

            # Redirect user to next page?
            if request.POST.get('register_next', '0') == '1':
                response = HttpResponseRedirect(reverse('account.views.register_profile'))
                response.set_cookie('login_username', email, max_age=settings.SESSION_REMEMBER_EXPIRITY)

                return response
    else:
        form = RegisterGoForm(has_password=has_password)

    return render(request, 'account/account_register_go.jade', {
        'form': form,
        'current_step': 'go',
        'comment_pool': request.session.get('comment_pool', {}),
    })


@reg_required
def register_profile(request):
    """
    Account > Register Profile
    """
    user = request.user

    # Initiate data
    profile = Profile.objects.get_or_create(user=user)[0]
    register = Register.objects.get_or_create(user=user)[0]

    initial = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'city': profile.city,
        'country': profile.country,
    }

    # Save data?
    if request.method == 'POST' and request.POST.get('current_step') == 'profile':
        form = RegisterProfileForm(request.POST, initial=initial)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            # Update username
            UserFactory(user).update_username(first_name, last_name)

            # Update first name and last name
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Store profile
            profile.city = form.cleaned_data['city']
            profile.country = form.cleaned_data['country']
            profile.save()

            # Update register data
            register.step_current = 2
            register.ip_update = request.META['REMOTE_ADDR']
            register.save()

            # Redirect user to next page?
            if request.POST.get('register_next', '0') == '1':
                return HttpResponseRedirect(reverse('account.views.register_about'))
    else:
        form = RegisterProfileForm(initial=initial)
    
    return render(request, 'account/account_register_profile.jade', {
        'form': form,
        'current_step': 'profile',
        'register_resumed': RegisterHelper.is_resumed(request),
        'comment_pool': request.session.get('comment_pool', {}),
    })


@reg_required
def register_about(request):
    """
    Account > Register About
    """
    user = request.user

    # Initiate data
    profile = Profile.objects.get_or_create(user=user)[0]
    register = Register.objects.get_or_create(user=user)[0]

    initial = {
        'specialty': profile.specialty,
        'company': profile.company,
        'freelancing': profile.freelancing,
        'hiring': profile.hiring,
    }

    # Save data?
    if request.method == 'POST' and request.POST.get('current_step') == 'about':
        form = RegisterAboutForm(request.POST, initial=initial)

        if form.is_valid():
            specialty = form.cleaned_data['specialty']
            company = form.cleaned_data['company']
            freelancing = form.cleaned_data['freelancing']
            hiring = form.cleaned_data['hiring']

            # Update profile data
            profile.register_complete = True
            profile.specialty = specialty
            profile.company = company
            profile.freelancing = freelancing
            profile.hiring = hiring
            profile.save()

            # Create the rank record and upgrade experience
            RankProcessHelper.create(
                profile,
                None,
                [user.id, 'user'],
                RankHelper.get_action_by_name('registration_complete'),
            )

            # Update register data
            register.step_current = 3
            register.ip_update = request.META['REMOTE_ADDR']
            register.save()

            # Redirect user to next page?
            if request.POST.get('register_next', '0') == '1':
                return HttpResponseRedirect(reverse('account.views.register_done'))
        
        if request.POST.get('register_prev', '0') == '1':
            register.step_current = 1
            register.save()

            return HttpResponseRedirect(reverse('account.views.register_profile'))
    else:
        form = RegisterAboutForm(initial=initial)

    return render(request, 'account/account_register_about.jade', {
        'form': form,
        'current_step': 'about',
        'register_resumed': RegisterHelper.is_resumed(request),
        'comment_pool': request.session.get('comment_pool', {})
    })


@reg_required
def register_done(request):
    """
    Account > Register Done
    """
    user = request.user

    if request.method == 'POST':
        # Initiate data
        profile = Profile.objects.get_or_create(user=user)[0]
        register = Register.objects.get_or_create(user=user)[0]

        # Update register data
        register.complete = True
        register.step_current = 0
        register.date_complete = datetime.now()
        register.ip_complete = request.META['REMOTE_ADDR']
        register.save()

        # Update profile data
        profile.register_complete = True
        profile.save()

        # E-Mail confirmation process
        if not profile.email_verified:
            ConfirmHelper.send(request)

        redirect_to = request.session.get('comment_posted_url', None)

        if redirect_to is not None:
            return HttpResponseRedirect(redirect_to)

        return HttpResponseRedirect(reverse('home.views.root'))

    # Publish comment there
    move_comment_pool(request, user)
    comment_posted = True if request.session.get('comment_posted_url', None) else False

    return render(request, 'account/account_register_done.jade', {
        'current_step': 'done',
        'register_resumed': RegisterHelper.is_resumed(request),
        'email_contact': settings.EMAIL_CONTACT,
        'comment_posted': comment_posted
    })


# -- Confirm: Responses --
def confirm_key(request, uidb36, token, random):
    """
    Account > Confirm Key
    """
    confirm_res = ConfirmHelper.validate(uidb36, token, random)
    confirm_success = confirm_res[0]
    confirmed_now = confirm_res[1]
    confirm_user_id = confirm_res[2]

    # Key does not exist
    if confirm_success is False:
        raise Http404

    # Login the user (if not already authenticated)
    if not request.user.is_authenticated():
        user = get_user(user_id=confirm_user_id)

        if user is not None:
            request.session.set_expiry(settings.SESSION_REMEMBER_EXPIRITY)
            LoginHelper.login(request, user)

    if confirmed_now:
        request.session['alert'] = 'confirm_done_now'

    return HttpResponseRedirect(reverse('home.views.root'))


@auth_required
def confirm_retry(request, next=None):
    """
    Account > Confirm Retry
    """
    # This will invalidate previous confirm request and resend a new one
    ConfirmHelper.send(request)
    request.session['alert'] = 'confirm_pending_resent'

    next = next or request.GET.get('next', None)
    if next:
        return HttpResponseRedirect(unquote(next))

    return HttpResponseRedirect(reverse('home.views.root'))


# -- Settings: Responses --
@auth_required
def settings_root(request):
    """
    Account > Settings Root
    """
    form_saved = False
    social_cannot_disconnect = request.GET.get('social_cannot_disconnect', None) is not None
    social_cannot_connect = request.GET.get('social_cannot_connect', None) is not None

    user = request.user
    uid = user.id
    email = request.user.email

    instance_profile = Profile.objects.get(user=user)
    instance_user = get_user(user_id=uid)

    if request.method == 'POST':
        form_profile = SettingsRootProfileForm(request.POST, instance=instance_profile)
        form_user = SettingsRootUserForm(request.POST, instance=instance_user, uid=uid)

        if form_profile.is_valid() and form_user.is_valid():
            form_profile.save()

            if instance_user is not None:
                form_user.save()

                # Update username
                UserFactory(instance_user).update_username(
                    form_user.cleaned_data['first_name'],
                    form_user.cleaned_data['last_name'],
                )

                # Send the email changed notification?
                email_updated = form_user.cleaned_data['email']

                if email != email_updated:
                    ConfirmHelper.send(request, email=email_updated)
                    settings_email_changed_email(request)

            form_saved = True
    else:
        form_profile = SettingsRootProfileForm(instance=instance_profile)
        form_user = SettingsRootUserForm(instance=instance_user, uid=uid)

    # Get social account associations
    social_associations = [social.provider for social in instance_user.social_auth.all()]

    try:
        social_avatar_binding_id = instance_user.binding.source
    except AvatarBinding.DoesNotExist:
        social_avatar_binding_id = 'gravatar'

    social_avatar_binding = {
        'id': social_avatar_binding_id,
        'name': settings.SOCIAL_AUTH_BACKENDS.get(
            social_avatar_binding_id,
            social_avatar_binding_id.title()
        )
    }

    return render(request, 'account/account_settings_root.jade', {
        'user': instance_user,
        'form_profile': form_profile,
        'form_user': form_user,
        'form_saved': form_saved,
        'social_backends': settings.SOCIAL_AUTH_BACKENDS,
        'social_associations': social_associations,
        'social_avatar_binding': social_avatar_binding,
        'social_cannot_disconnect': social_cannot_disconnect,
        'social_cannot_connect': social_cannot_connect,
    })


@auth_required
def settings_credentials(request):
    """
    Account > Settings Credentials
    """
    form_saved = False

    if request.method == 'POST':
        form = SettingsCredentialsForm(request.user, request.POST)

        if form.is_valid() and form.cleaned_data['new_password']:
            # Change password
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()

            # Notify the user
            settings_credentials_changed_email(request)
            form_saved = True
    else:
        form = SettingsCredentialsForm(request.user)

    return render(request, 'account/account_settings_credentials.jade', {
        'form': form,
        'form_saved': form_saved,
    })


@auth_required
def settings_notifications(request):
    """
    Account > Settings Notification
    """
    form_saved = False
    instance = Settings.objects.get_or_create(
        user=request.user
    )[0]

    response_data = NotificationHelper.build_response_page(
        request=request,
        items_per_page=10,
    )

    if request.method == 'POST':
        form = SettingsNotificationForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            form_saved = True
    else:
        form = SettingsNotificationForm(instance=instance)

    response_data.update({
        'form': form,
        'form_saved': form_saved,
    })

    return render(request, 'account/account_settings_notifications.jade', response_data)


@auth_required
def settings_notifications_fetch(request, page=1):
    """
    Account > Settings Notification Fetch
    """
    page = int(page)
    items_per_page = 10

    response_data = NotificationHelper.build_response_page(
        request=request,
        page=page,
        items_per_page=items_per_page,
    )

    if len(response_data['notification_feed']) or page is 1:
        return render(request, 'account/account_settings_notifications_fetch.jade', response_data)
    
    return HttpResponse(
        json.dumps({
            'status': 'error',
            'message': 'Page overflow',
            'contents': {}
        }),
        content_type='application/json'
    )


@auth_required
def settings_ajax_avatar(request):
    """
    Account > Settings AJAX (Avatar)
    """
    response_data = {
        'status': 'error',
        'message': '',
        'contents': {}
    }

    if request.method == 'POST':
        source = request.POST.get('source', None)

        if not source:
            response_data['message'] = 'No Source Provided'
        else:
            try:
                AvatarHelper.update(request.user, source=source)
                response_data['contents']['url'] = '{host}{username}/?circle&{timestamp}'.format(
                    host=settings.AVATAR_URL,
                    username=request.user.username,
                    timestamp=int(time()),
                )

                response_data['status'] = 'success'
            except Exception as e:
                response_data['message'] = str(e)
    else:
        response_data['message'] = 'Bad Request'

    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json'
    )


# -- Recover: Responses --
@anon_required
def recover_root(request):
    """
    Account > Recover Root
    """
    error_notif = {
        'has': False,
        'short': None,
        'long': None
    }
    form_success = False

    # Save data?
    if request.method == 'POST':
        form = RecoverRootForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']

            user = get_user(username=username, email=username)

            if user is not None:
                RecoverHelper.send(request, user)
                form_success = True
                form.fields['username'].widget.attrs['disabled'] = 'disabled'
            else:
                error_notif['has'] = True
                error_notif['short'] = 'User not found.'
                error_notif['long'] = 'We could not find an account with that email.'
        else:
            error_notif['has'] = True
            error_notif['short'] = 'Invalid email.'
            error_notif['long'] = 'Please enter a valid email address.'
    else:
        if request.session.get('recover_expired', False) is True:
            del request.session['recover_expired']
            error_notif['has'] = True
            error_notif['short'] = 'Key has expired.'
            error_notif['long'] = 'This recovery key has expired. Please retry.'

        login_username = request.COOKIES.get('login_username', None)
        form = RecoverRootForm(initial={'username': login_username})

    return render(request, 'account/account_recover_root.jade', {
        'form': form,
        'error_notif': error_notif,
        'form_success': form_success,
    })


@anon_required
def recover_key(request, uidb36, token, random):
    """
    Account > Recover Key
    """
    recover_res = RecoverHelper.validate(uidb36, token, random)
    recover_success = recover_res[0]
    recover_expired = recover_res[1]
    recover_user_id = recover_res[2]

    # Key does not exist
    if recover_success is False:
        if recover_expired is True:
            request.session['recover_expired'] = True
            return HttpResponseRedirect(reverse('account.views.recover_root'))
        
        raise Http404

    # Login the user (if not already authenticated)
    if not request.user.is_authenticated():
        user = get_user(user_id=recover_user_id)

        if user is not None:
            request.session.set_expiry(settings.SESSION_REMEMBER_EXPIRITY)
            LoginHelper.login(request, user)

    return HttpResponseRedirect(reverse('account.views.recover_proceed'))


@auth_required
def recover_proceed(request):
    """
    Account > Recover Proceed
    """
    error_notif = {
        'has': False,
        'short': None,
        'long': None
    }

    # Save data?
    if request.method == 'POST':
        form = RecoverProceedForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']

            if password == password_confirm:
                request.user.set_password(password)
                request.user.save()

                request.session['alert'] = 'recover_done_now'
                return HttpResponseRedirect(reverse('home.views.root'))
            else:
                error_notif['has'] = True
                error_notif['short'] = 'Passwords do not match.'
                error_notif['long'] = 'The passwords do not match. Please enter them again.'
        else:
            error_notif['has'] = True
            error_notif['short'] = 'Invalid password.'
            error_notif['long'] = 'Invalid password, enter one between %s and %s chars.'\
                                    % (defaults.PWD_LENGTH_MIN, defaults.PWD_LENGTH_MAX,)
    else:
        form = RecoverProceedForm()

    return render(request, 'account/account_recover_proceed.jade', {
        'form': form,
        'error_notif': error_notif,
    })
