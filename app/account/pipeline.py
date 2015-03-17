import social, facebook

from django.conf import settings

from _commons.helpers.countries import CountriesHelper
from avatar.models import Binding as AvatarBinding
from comment.helpers import PoolHelper
from avatar.helpers import AvatarHelper

from .models import *
from .factories import *


def get_username(backend, uid, details, strategy, user=None, *args, **kwargs):
    """
    Gets the user username from social account data
    """
    if not user:
        first_name = details.get('first_name', None)
        last_name = details.get('last_name', None)

        if (first_name and last_name) or (uid and backend):
            final_username = UserFactory(user).generate_username(
                first_name=first_name,
                last_name=last_name,
                uid=uid,
                backend=backend,
            )
        else:
            raise Exception('Could Not Generate Username (First Name/Last Name/UID/Backend Missing)')
    else:
        final_username = strategy.storage.user.get_username(user)
    
    return {
        'username': final_username
    }


def update_user_avatar(backend, response, user, is_new=False, *args, **kwargs):
    """
    Updates the user avatar from social account
    """
    if is_new and user:
        AvatarHelper.update(user, source=backend.name)


def fill_profile_user(backend, response, details, user, is_new=False, *args, **kwargs):
    """
    Auto-confirm user that comes from a social API
    """
    if is_new and user and user.is_authenticated():
        social_user = user.social_auth.filter(provider=backend.name).first()

        if not social_user:
            raise Exception("Social User Binding Not Found")

        # Get models
        profile = Profile.objects.get_or_create(user=user)[0]
        register = Register.objects.get_or_create(user=user)[0]

        if backend.name == 'facebook':
            # Get data from Facebook Graph
            graph = facebook.GraphAPI(social_user.extra_data['access_token'])
            graph_data = graph.fql('SELECT {rows} FROM {table} WHERE uid=me()'.format(
                rows=', '.join([
                    'first_name',
                    'last_name',
                    'current_location',
                    'hometown_location',
                    'work',
                    'education',
                    'website',
                    'verified'
                ]),
                table='user',
            ))

            if len(graph_data):
                graph_data = graph_data[0]
            else:
                raise Exception("Got No Response Data From Facebook Graph")

            # Get user first name & last name
            user.first_name = graph_data['first_name'].strip().title()
            user.last_name = graph_data['last_name'].strip().title()

            # Get city & country
            profile_country = None

            if 'current_location' in graph_data:
                profile.city = graph_data['current_location']['city'].strip().title()
                profile_country = graph_data['current_location']['country'].strip().title()
            elif 'hometown_location' in graph_data:
                profile.city = graph_data['hometown_location']['city'].strip().title()
                profile_country = graph_data['hometown_location']['country'].strip().title()

            if profile_country:
                profile_country_iso2 = CountriesHelper.get_iso2_from_name(profile_country)
                if profile_country_iso2:
                    profile.country = profile_country_iso2

            # Get specialty & company
            if 'work' in graph_data and len(graph_data['work']):
                work = graph_data['work'][len(graph_data['work']) - 1]

                if 'position' in work:
                    profile.specialty = work['position']['name'].strip().title()
                if 'employer' in work:
                    profile.company = work['employer']['name'].strip().title()
            elif 'education' in graph_data and len(graph_data['education']):
                education = graph_data['education'][len(graph_data['education']) - 1]

                if 'type' in education:
                    profile.specialty = '%s Student' % (education['type'])
                if 'school' in education:
                    profile.company = education['school']['name'].strip().title()

            # Get website
            if 'website' in graph_data:
                profile.website = graph_data['website'].strip()

            # Get email verified state (we trust Facebook)
            profile.email_verified = profile.email_verified or (graph_data['verified'] and True)
        elif backend.name == 'twitter':
            # Set user first name & last name
            user.first_name = details.get('first_name').strip().title()
            user.last_name = details.get('last_name').strip().title()
        elif backend.name == 'google-oauth2':
            pass
        else:
            raise ValueError()

        # Check for registration form status
        if not user.first_name or not user.last_name or not user.email:
            register.step_current = 0
        elif not profile.city or not profile.country:
            register.step_current = 1
        elif not profile.specialty or not profile.company:
            register.step_current = 2
        else:
            register.step_current = 3

        # Store data
        profile.save()
        register.save()
        user.save()


def move_comment_pool(request, user, *args, **kwargs):
    """
    Move comments from pool on user login
    """
    if user:
        comment_pool = request.session.get('comment_pool', {})

        if comment_pool:
            comment_pool_next_url, comment_pool_next_id = PoolHelper.move(request, user, comment_pool)

            if comment_pool_next_url and comment_pool_next_id:
                comment_pool_final_url = '%s#comment-%s' % (comment_pool_next_url, comment_pool_next_id)

                request.session['alert'] = 'comment_posted_now'
                request.session['alert_data'] = comment_pool_final_url
                request.session['comment_posted_url'] = comment_pool_final_url
            else:
                request.session['alert'] = 'comment_posted_error'


def remove_avatar_binding(backend, user, *args, **kwargs):
    """
    Removes the social account avatar binding (if set to disconnected backend)
    """
    if backend and user:
        try:
            if user.binding.source == backend.name:
                # Re-initialize avatar to initial state
                AvatarHelper.initialize(user)
        except AvatarBinding.DoesNotExist:
            pass
