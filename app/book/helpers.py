from hitcount.utils import count_hits as hitcount_count_hits
from django.conf import settings
from django.core.urlresolvers import reverse

from _commons.helpers.fields import FieldsHelper
from _commons.helpers.cache import CacheHelper
from _commons.helpers.numbers import percentage_of

from comment.helpers import MetaHelper as CommentMetaHelper
from relevance.helpers import RelevanceHelper


class BookHelper(object):
    """
    An helper on book operations
    """

    @staticmethod
    def resolve(book_id):
        """
        Resolve a book by ID
        """
        from models import Item

        try:
            return Item.objects.get(id=book_id, is_visible=True)
        except Item.DoesNotExist:
            return None


    @staticmethod
    def list():
        """
        List available books
        """
        from models import Item

        return Item.objects.filter(is_visible=True)


    @staticmethod
    def list_with_tag(tag):
        """
        Return the books that are tagged with provided tag
        """
        from models import Tag
        
        return [t.book for t in Tag.objects.filter(tag=tag)]


    @staticmethod
    def title(book):
        """
        Return a book title
        """
        return book.title


    @classmethod
    def relevance(_class, book, request=None):
        """
        Calculate a book's relevance arguments
        """
        return RelevanceHelper.get(
            'book',
            book.id,
            (request.user if request else None),
        )
    

    @classmethod
    def views(_class, book):
        """
        Return a book number of views
        """
        return hitcount_count_hits(book)
    

    @classmethod
    def reviews(_class, book):
        """
        Return the number of reviews on given book
        """
        return CommentMetaHelper.count('book', book.id)


    @staticmethod
    def url(book):
        """
        Return a book real URL
        """
        return book.url_set.filter(is_alias=False).first()


    @classmethod
    def url_full(_class, book):
        """
        Return the full (reversed) URL to book
        """
        book_url = _class.url(book)

        if book_url and book_url.author and book_url.slug:
            return reverse('book.views.view', kwargs={
                'author': book_url.author,
                'slug': book_url.slug,
            })

        return ''


    @staticmethod
    def amazon_url(book):
        """
        Return usable book Amazon URL
        """
        url = ''

        if book.amazon_id:
            url = '%s/gp/product/%s' % (settings.AMAZON_URL, book.amazon_id)

            if settings.AMAZON_AFFILIATE_ID:
                url += '/ref=as_li_ss_tl?tag=%s' % settings.AMAZON_AFFILIATE_ID

        return url


    @staticmethod
    def check(fn_name, author, slug):
        """
        Checks book data
        """
        from models import Url

        book, status, path = None, 'not_found', None
        
        try:
            book_url = Url.objects.get(author=author, slug=slug)

            if book_url.is_alias is True:
                # Resolve associated URL that is not an alias
                book_alias = Url.objects.get(book_id=book_url.book_id, is_alias=False)

                book = book_url.book
                status = 'redirect'
                path = reverse('book.views.' + fn_name, kwargs={
                    'author': book_alias.author,
                    'slug': book_alias.slug,
                })
            else:
                book = book_url.book
                status = 'visible' if book.is_visible else 'not_visible'
        except Url.DoesNotExist:
            pass
        finally:
            return book, status, path


    @classmethod
    def generate_data(_class, book):
        """
        Generates book data
        """
        return {
            'item': book,
            'amazon_url': _class.amazon_url(book),
            'relevance': _class.relevance(book),
            'views': _class.views(book),
            'reviews': _class.reviews(book),
            'url': _class.url(book),
        }


    @staticmethod
    def get_cover_path(variant, instance, filename):
        """
        Returns the cover path for given book
        """
        name = filename.split('.')[0]
        extension = filename.split('.')[-1]

        return os.path.join(
            'books',
            instance.id,
            '%s.%s' % (slugify(instance.name), slugify(instance.extension),)
        )


    @classmethod
    def get_cover_path_original(_class, instance, filename):
        """
        Returns the original cover path for given book
        """
        return _class.get_cover_path('original', instance, filename)


    @classmethod
    def get_cover_path_small(_class, instance, filename):
        """
        Returns the small cover path for given book
        """
        return _class.get_cover_path('small', instance, filename)


    @classmethod
    def get_cover_path_medium(_class, instance, filename):
        """
        Returns the medium cover path for given book
        """
        return _class.get_cover_path('medium', instance, filename)


    @classmethod
    def get_cover_path_large(_class, instance, filename):
        """
        Returns the large cover path for given book
        """
        return _class.get_cover_path('large', instance, filename)


    @staticmethod
    def get_cover_absolute_url(path):
        """
        Returns the absolute URL to given cover path
        """
        return '%s%s' % (settings.MEDIA_URL, path)


    @classmethod
    def suggestions(_class, user, maximum=1):
        """
        Suggests a set of books
        """
        namespace = CacheHelper.ns('book:helpers:suggestions', user, maximum=maximum)
        results = CacheHelper.io.get(namespace)

        if results is None:
            results = []

            for book in FieldsHelper.random(_class.list(), maximum):
                results.append(
                    _class.generate_data(book)
                )

            CacheHelper.io.set(namespace, results, 60)

        return results
