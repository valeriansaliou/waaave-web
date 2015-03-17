import os
from datetime import datetime, timedelta
from django.contrib.auth.models import User as AuthUser

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import load_backend, login
from django.contrib.auth.tokens import default_token_generator as token_generator

from _commons.helpers.fields import FieldsHelper
from _commons.helpers.cache import CacheHelper

from .models import *
from .emails import *



class UserHelper(object):
    """
    An helper on user operations
    """

    @staticmethod
    def suggestions(user, maximum=1, ignore_user=None):
        """
        Suggests a set of users
        """
        namespace = CacheHelper.ns(
            'account:helpers:user:suggestions',
            user,
            maximum=maximum,
            ignore_user_id=(ignore_user.id if ignore_user else None)
        )
        results = CacheHelper.io.get(namespace)

        if results is None:
            results = []
            filtered = AuthUser.objects.filter(profile__rank__gt=5)

            if ignore_user:
                filtered = filtered.exclude(id=ignore_user.id).exclude(follow__follower=ignore_user.id)

            for user in FieldsHelper.random(filtered, maximum):
                results.append({
                    'user': user,
                    'profile': user.profile,
                })

            CacheHelper.io.set(namespace, results, 20)

        return results



class LoginHelper(object):
    """
    An helper on login operations
    """

    @staticmethod
    def login(request, user):
        """
        Login a given user
        """
        # Login user w/o required credentials (but rather the model object)
        if not hasattr(user, 'backend'):
            for backend in settings.AUTHENTICATION_BACKENDS:
                if user == load_backend(backend).get_user(user.pk):
                    user.backend = backend
                    break
        if hasattr(user, 'backend'):
            return login(request, user)



class RegisterHelper(object):
    """
    An helper on register operations
    """

    steps = [
        'go',
        'profile',
        'about',
        'done'
    ]


    @classmethod
    def step_name(_class, step_id):
        """
        Return the register step name associated to a step ID
        """
        try:
            assert type(step_id) is int
            return _class.steps[step_id]
        except IndexError:
            return _class.steps[1]


    @classmethod
    def step(_class, request):
        """
        Return the current register step
        """
        step_current = 1

        try:
            step_current = Register.objects.get(user=request.user).step_current
        except Register.DoesNotExist:
            pass
        finally:
            return _class.step_name(step_current)


    @staticmethod
    def update_resume(request):
        """
        Increment the 'registration resumed' counter
        """
        resumed_count = 0

        try:
            register = Register.objects.get(user=request.user)
            resumed_count = register.resumed_count
            register.resumed_count += 1
            register.save()
        except Register.DoesNotExist:
            pass
        finally:
            return resumed_count


    @staticmethod
    def is_resumed(request):
        """
        Return whether registration was resumed or not
        """
        try:
            return True if (Register.objects.get(user=request.user).resumed_count > 0) else False
        except Register.DoesNotExist:
            return False



class ConfirmHelper(object):
    """
    An helper on confirm operations
    """

    @staticmethod
    def send(request, email=None):
        """
        Send the account confirm email
        """
        key = token_generator.make_token(request.user)

        # Split the key
        try:
            key_uidb36, key_token = key.split('-')
        except ValueError:
            return False

        # Generate a random (additional) key
        key_random = os.urandom(20).encode('hex')

        # Store in DB
        confirm = Confirm.objects.filter(user=request.user).delete()

        Confirm(
            user=request.user,
            key_uidb36=key_uidb36,
            key_token=key_token,
            key_random=key_random,
        ).save()

        # Send email
        confirm_email(request, key_uidb36, key_token, key_random, email=email)

        return True


    @staticmethod
    def validate(key_uidb36, key_token, key_random):
        """
        Confirm the user account
        """
        values = False, False, None

        try:
            confirm = Confirm.objects.get(key_uidb36=key_uidb36, key_token=key_token, key_random=key_random)

            if not confirm.confirmed:
                confirmed_now = True

                confirm.confirmed = True
                confirm.date_confirmed = datetime.now()
                confirm.save()
            else:
                confirmed_now = False
            
            values = True, confirmed_now, confirm.user_id
        except Confirm.DoesNotExist:
            pass
        finally:
            return values



class RecoverHelper(object):
    """
    An helper on recover operations
    """

    @staticmethod
    def send(request, user):
        """
        Send the account recovery email
        """
        key = token_generator.make_token(user)

        # Split the key
        try:
            key_uidb36, key_token = key.split('-')
        except ValueError:
            return False

        # Generate a random (additional) key
        key_random = os.urandom(20).encode('hex')

        expire_minutes = 30
        date_expire = datetime.now() + timedelta(minutes=30)

        # Store in DB
        Recover.objects.filter(user=user).delete()

        Recover(
            user=user,
            date_expire=date_expire,
            key_uidb36=key_uidb36,
            key_token=key_token,
            key_random=key_random,
        ).save()

        # Send email
        recover_email(request, user.email, expire_minutes, key_uidb36, key_token, key_random)

        return True


    @staticmethod
    def validate(key_uidb36, key_token, key_random):
        """
        Validate the account recovery keys
        """
        values = False, False, None

        try:
            recover = Recover.objects.get(key_uidb36=key_uidb36, key_token=key_token, key_random=key_random)

            # Key expired?
            date_now = datetime.now()

            if recover.recovered or date_now >= recover.date_expire:
                values = False, True, None
            else:
                recover.recovered = True
                recover.date_recovered = date_now
                recover.save()

                values = True, False, recover.user_id
        except Recover.DoesNotExist:
            pass
        finally:
            return values



class SettingsHelper(object):
    """
    An helper on settings operations
    """

    @staticmethod
    def __get(field, user_id):
        """
        Get the requested setting
        """
        value = Settings._meta.get_field_by_name(field)[0].default or False

        try:
            settings = Settings.objects.filter(user_id=user_id).values()[0]
            value = settings[field]
        except ObjectDoesNotExist:
            pass
        finally:
            return value


    @classmethod
    def has_email_respond(_class, user_id):
        """
        Get the email respond value for given user
        """
        return _class.__get('email_respond', user_id)


    @classmethod
    def has_email_follow(_class, user_id):
        """
        Get the email follow value for given user
        """
        return _class.__get('email_follow', user_id)


    @classmethod
    def has_email_follow_add(_class, user_id):
        """
        Get the email follow add value for given user
        """
        return _class.__get('email_follow_add', user_id)


    @classmethod
    def has_notif_respond(_class, user_id):
        """
        Get the email notification respond value for given user
        """
        return _class.__get('notif_respond', user_id)


    @classmethod
    def has_notif_spot(_class, user_id):
        """
        Get the email notification spot value for given user
        """
        return _class.__get('notif_spot', user_id)


    @classmethod
    def has_notif_follow(_class, user_id):
        """
        Get the email notification respond value for given user
        """
        return _class.__get('notif_follow', user_id)


    @classmethod
    def has_notif_follow_add(_class, user_id):
        """
        Get the email notification respond value for given user
        """
        return _class.__get('notif_follow_add', user_id)


    @classmethod
    def has_notif_waaave(_class, user_id):
        """
        Get the email notification respond value for given user
        """
        return _class.__get('notif_waaave', user_id)
