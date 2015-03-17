from hashlib import md5

from django.template.defaultfilters import slugify
from django.contrib.auth.models import User as AuthUser

from _commons.helpers.strings import StringsHelper

from .models import *


class UserFactory:
    """
    Allows for user creation, management and removal
    """
    
    def __init__(self, user=None):
        self.__user = user


    @staticmethod
    def generate_username(first_name=None, last_name=None, email=None, uid=None, backend='internal'):
        """
        Generate user username
        """
        assert (first_name and last_name) or email or uid

        if first_name and last_name:
            first_name, last_name = StringsHelper.downcode(first_name), StringsHelper.downcode(last_name)
            first_name, last_name = slugify(first_name), slugify(last_name)
            
            # First attempt: {first_name.last_name}
            username = '%s.%s' % (first_name.replace(' ', '.'), last_name.replace(' ', '.'))
            base_username = username

            if AuthUser.objects.filter(username=username).count() > 0:
                # Second attempt: {first_name.last_name.i}
                users = AuthUser.objects.filter(username__iregex=r'{0}.[0-9]+$'.format(base_username)).order_by('username').values('username')

                if len(users) > 0:
                    last_number_used = [int(u['username'].replace('{0}.'.format(base_username), '')) for u in users]
                    last_number_used.sort()
                    last_number_used = last_number_used[-1]

                    number = last_number_used + 1
                    username = '%s.%s' % (base_username, number)
                else:
                    number = 1

                username = '%s.%s' % (base_username, number)

            return username

        digest = email or ('%s-%s' % (backend, uid))
        
        return md5(digest).hexdigest()[:30]


    def create(self, email, password):
        """
        Create a new user with provided email and password
        """
        assert self.__user is None

        # Check user does not already exist
        if AuthUser.objects.filter(email=email).count():
            raise Exception('E-Mail Already Taken')

        # Create user
        user = AuthUser.objects.create_user(
            self.generate_username(email=email),
            email,
            password,
        )
        user.save()

        self.__user = user

        # Initiate user settings & profile
        Profile(user=user).save()
        Settings(user=user).save()

        return True


    def remove(self):
        """
        Remove user
        """
        pass


    def update_username(self, first_name, last_name):
        """
        Generate user username
        """
        assert first_name and last_name and self.__user

        # Update only if first name/last name changed
        if not (self.__user.first_name == first_name and self.__user.last_name == last_name):
            username = self.generate_username(
                first_name=first_name,
                last_name=last_name,
            )

            self.__user.username = username
            self.__user.save()

        return True


    def get_user(self):
        """
        Return user object
        """
        return self.__user


    def set_user(self, user):
        """
        Update user object
        """
        self.__user = user
