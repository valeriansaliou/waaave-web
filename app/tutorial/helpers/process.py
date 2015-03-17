from hitcount.utils import count_hits as hitcount_count_hits
from django.core.urlresolvers import reverse

from _commons.helpers.statuses import StatusesHelper

from tutorial.models import *



class ProcessHelper(object):
    """
    An helper on process operations
    """

    @staticmethod
    def duration(content, level):
        """
        Return the estimated duration of a tutorial
        """
        return int(float(len(content)) * 0.60\
                 * (float(level + 1) * 0.25))
    

    @classmethod
    def views(_class, tutorial):
        """
        Return a tutorial number of views
        """
        return hitcount_count_hits(tutorial)


    @staticmethod
    def url(tutorial_id):
        """
        Return a tutorial real URL
        """
        tut_url = {
            'tag': None,
            'slug': None,
        }

        try:
            if tutorial_id:
                tutorial_alias = Url.objects.get(tutorial_id=tutorial_id, is_alias=False)

                tut_url['tag'] = tutorial_alias.tag
                tut_url['slug'] = tutorial_alias.slug
        except Url.DoesNotExist:
            pass
        finally:
            return tut_url


    @classmethod
    def url_full(_class, tutorial_id):
        """
        Return the full (reversed) URL to tutorial
        """
        tut_url = _class.url(tutorial_id)

        if tut_url['tag'] and tut_url['slug']:
            return reverse('tutorial.views.view', kwargs={
                'tag': tut_url['tag'],
                'slug': tut_url['slug'],
            })

        return ''


    @staticmethod
    def title(tutorial_id):
        """
        Return a tutorial title
        """
        tut_title = None

        try:
            if tutorial_id:
                tut_title = Meta.objects.get(id=tutorial_id).title
        except Author.DoesNotExist:
            pass
        finally:
            return tut_title


    @staticmethod
    def author(tutorial_id):
        """
        Return a tutorial author (master)
        """
        tut_author = None

        try:
            if tutorial_id:
                tut_author = Author.objects.get(tutorial_id=tutorial_id, is_master=True).user_id
        except Author.DoesNotExist:
            pass
        finally:
            return tut_author


    @staticmethod
    def authors_all(tutorial_id):
        """
        Return tutorial authors (master + contributors)
        """
        return Author.objects.filter(tutorial_id=tutorial_id)


    @staticmethod
    def check(fn_name, tag, slug):
        """
        Check given tutorial data
        """
        status = None, 'not_found', None

        try:
            tutorial_url = Url.objects.get(tag=tag, slug=slug)

            if tutorial_url.is_alias is True:
                tutorial_alias = Url.objects.get(tutorial_id=tutorial_url.tutorial_id, is_alias=False)

                status = tutorial_url.tutorial_id, 'redirect', reverse('tutorial.views.' + fn_name, kwargs={
                    'tag': tutorial_alias.tag,
                    'slug': tutorial_alias.slug,
                })
            else:
                tutorial = tutorial_url.tutorial

                if tutorial.is_visible():
                    status = tutorial.id, 'exists', None
                else:
                    status = tutorial.id, 'unpublished', None
        except Url.DoesNotExist:
            pass
        finally:
            return status


    @classmethod
    def generate_data(_class, tutorial, author=None):
        """
        Generates tutorial data
        """
        # This import prevents circular imports as this file is used in RelevanceHelper
        from relevance.helpers import RelevanceHelper

        author = author or tutorial.author_set.filter(is_master=True).first()

        return {
            'user': author.user,
            'meta': tutorial,
            'title': tutorial.title,
            'body': tutorial.content.body,
            'relevance': RelevanceHelper.get('tutorial', tutorial.id),
            'views': _class.views(tutorial),
            'url': _class.url(tutorial.id),
        }
