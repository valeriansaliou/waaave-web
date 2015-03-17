from django.contrib.auth.models import User


def get_user(username=None, email=None, user_id=None):
    try:
        if username is not None:
            return User.objects.get(username=username)
        raise User.DoesNotExist()
    except User.DoesNotExist:
        try:
            if email is not None:
                return User.objects.get(email=email)
            raise User.DoesNotExist()
        except User.DoesNotExist:
            try:
                if user_id is not None:
                    return User.objects.get(id=user_id)
                raise User.DoesNotExist()
            except User.DoesNotExist:
                return None
    return None