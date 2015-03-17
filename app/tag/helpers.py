from django.template.defaultfilters import slugify
from django.conf import settings

from .settings import *


class TagHelper(object):
    """
    An helper on tag operations
    """

    @staticmethod
    def unpack(tags):
        """
        Unpack the user submitted list of tags (string to list)
        """
        return tags.split(',')


    @staticmethod
    def normalize(tags):
        """
        Normalize a list of tags (slug,name)
        """
        normalized = []

        for cur_tag in tags:
            cur_tag = cur_tag.strip().lower()
            cur_name = cur_tag.title()
            cur_tag_slug = slugify(cur_tag)
            
            if cur_name and cur_tag_slug:
                normalized.append((cur_tag_slug,cur_name,))

        return normalized


    @classmethod
    def string_to_list(_class, tags):
        """
        Full tags string to list conversion
        """
        return _class.normalize(_class.unpack(tags))


    @staticmethod
    def validate(tag):
        """
        Validate a given tag
        """
        return tag[0] is not ''\
                and tag[1] is not ''\
                and len(tag[0]) <= TAG_SLUG_MAX_LENGTH\
                and len(tag[1]) <= TAG_NAME_MAX_LENGTH


    @staticmethod
    def get_picture_path(variant, instance, filename):
        """
        Returns the picture path for given tag
        """
        name = filename.split('.')[0]
        extension = filename.split('.')[-1]

        return os.path.join(
            'tags',
            instance.id,
            '%s.%s' % (slugify(instance.name), slugify(instance.extension),)
        )


    @classmethod
    def get_picture_path_original(_class, instance, filename):
        """
        Returns the original picture path for given tag
        """
        return _class.get_picture_path('original', instance, filename)


    @classmethod
    def get_picture_path_small(_class, instance, filename):
        """
        Returns the small picture path for given tag
        """
        return _class.get_picture_path('small', instance, filename)


    @classmethod
    def get_picture_path_normal(_class, instance, filename):
        """
        Returns the normal picture path for given tag
        """
        return _class.get_picture_path('normal', instance, filename)


    @classmethod
    def get_picture_path_large(_class, instance, filename):
        """
        Returns the large picture path for given tag
        """
        return _class.get_picture_path('large', instance, filename)


    @staticmethod
    def get_picture_absolute_url(path):
        """
        Returns the absolute URL to given picture path
        """
        return '%s%s' % (settings.MEDIA_URL, path)
