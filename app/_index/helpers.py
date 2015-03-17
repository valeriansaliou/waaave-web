from django.core.urlresolvers import reverse

from _index.models import Ids as _IndexIds

from avatar.templatetags.avatar import avatar
from _commons.helpers.types import TypesHelper

from tutorial.models import Author as TutorialAuthor


class ContentHelper(object):
    """
    An helper on content operations
    """

    @staticmethod
    def get(item_id, item_type):
        """
        Get indexed content
        """
        index = None

        try:
            index = _IndexIds.objects.get(item_id=item_id, item_type=TypesHelper.encode(item_type))
        except _IndexIds.DoesNotExist:
            pass
        finally:
            return index

    
    @classmethod
    def validate(_class, item_id, item_type):
        """
        Validate indexed content
        """
        # Import some stuff there (prevents circular imports)
        from tutorial.helpers.process import ProcessHelper as TutorialProcessHelper

        content_exists, content_author_id = False, None
        index = _class.get(item_id, item_type)

        if index:
            content_exists = True
        
        item_type = TypesHelper.reverse(index.item_type) if content_exists else None

        if item_type == 'tutorial':
            content_author_id = TutorialProcessHelper.author(item_id)

        return content_exists, content_author_id


    @staticmethod
    def read(item):
        """
        Read indexed content data
        """
        # Import some stuff there (prevents circular imports)
        from tutorial.helpers.process import ProcessHelper as TutorialProcessHelper
        from book.helpers import BookHelper

        content_data = {
            'type': None,
            'id': None,
            'content': {},
            'author': {}
        }

        # Read content relations
        user = None

        if item is not None:
            content_data['id'] = item.item_id
            content_data['type'] = TypesHelper.reverse(item.item_type)
            
            content_data_url, content_data_title = None, None

            if content_data['type'] == 'tutorial':
                content_data_url = TutorialProcessHelper.url_full(content_data['id'])
                content_data_title = TutorialProcessHelper.title(content_data['id'])
            elif content_data['type'] == 'book':
                book = BookHelper.resolve(content_data['id'])

                if book:
                    content_data_url = BookHelper.url_full(book)
                    content_data_title = BookHelper.title(book)

            content_data['content'] = {
                'url': content_data_url,
                'title': content_data_title,
            }

        # Get author data
        if user is not None:
            profile = user.profile

            content_data['author'] = {
                'avatar': avatar(user),
                'rank': profile.rank,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'url': reverse('user.views.main', args=[user.username]),
                'specialty': profile.specialty,
            }

        return content_data
