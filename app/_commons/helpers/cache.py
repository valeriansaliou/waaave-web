from hashlib import md5

from django.core.cache import cache as cache_core
from _commons.helpers.strings import StringsHelper


class CacheHelper(object):
    """
    An helper on moderation operations
    """

    """
    Alias of the Django's cache instance
    """
    io = cache_core


    @staticmethod
    def ns(path, user=None, hash=True, **kwargs):
        """
        Returns generated cache namespace
        """
        args = u''

        for key, item in kwargs.iteritems():
            if args: args += '|'
            args += u'%s=%s' % (key, StringsHelper.strip_accents(item),)

        formatted = u'{0}[{1}]{2}'.format(
            path,
            ((user.id if user else None) or 'anonymous'),
            (u'(%s)' % args if args else u'')
        )

        if hash:
            formatted_normalized = formatted.encode('utf-8')
            return md5(formatted_normalized).hexdigest()

        return formatted
