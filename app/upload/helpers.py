import os

from django.utils.text import slugify


class UploadHelper(object):
    """
    An helper on upload operations
    """

    @staticmethod
    def get_upload_path(instance, filename):
        """
        Returns the upload path for given user
        """
        instance.name = filename.split('.')[0]
        instance.extension = filename.split('.')[-1]

        return os.path.join(
            'uploads',
            instance.user.username,
            '%s.%s' % (slugify(instance.name), slugify(instance.extension),)
        )
