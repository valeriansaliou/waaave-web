from django.core.exceptions import ObjectDoesNotExist

from _commons.helpers.statuses import StatusesHelper
from _commons.helpers.cache import CacheHelper

from tutorial.helpers.process import ProcessHelper as TutorialProcessHelper
from tutorial.models import Meta as TutorialMeta
from tutorial.models import Author as TutorialAuthor

from book.helpers import BookHelper
from spot.helpers import SpotHelper


class BaseExploreHelper(object):
    """
    An helper on explore common operations
    """

    @staticmethod
    def _read_items(*args, **kwargs):
        """
        Base items read class
        """
        raise NotImplementedError


    @staticmethod
    def _generate_data(*args, **kwargs):
        """
        Base data generation class
        """
        raise NotImplementedError


    @classmethod
    def _popular_data(_class, namespace, items_all, page, start, end):
        """
        Base popular method
        """
        filtered = CacheHelper.io.get(namespace)

        if filtered is None:
            # Process the popular data
            filtered = _class._popular_process(items_all)

            # Sort the items
            filtered = sorted(filtered, key=lambda tutorial: tutorial['popularity'], reverse=True)

            CacheHelper.io.set(namespace, filtered, 300)

        return filtered[start:end]


    @classmethod
    def _popular_process(_class, items_all):
        """
        Process popularity data
        popularity = views + 5 * relevant - 20 * irrelevant
        """
        processed = []

        # Compute the item popularity
        for item in items_all:
            item = _class._generate_data(item)

            item['popularity'] = int(item['views']\
                                 + (5 * item['relevance']['count_relevant'])\
                                 - (10 * item['relevance']['count_irrelevant']))
            
            processed.append(item)

        return processed


    @classmethod
    def build_response(_class, namespace, request, items_per_page=10, page=1, order_by=None, *args, **kwargs):
        """
        Builds the tutorials explore response data
        """
        response = CacheHelper.io.get(namespace)

        if response is None:
            page = int(page or 1)
            page = page or 1

            start = (page - 1) * items_per_page
            end = start + items_per_page

            items = []
            items_all = _class._read_items(*args, **kwargs)

            items_count = items_all.count() if items_all else 0
            page_total = items_count // items_per_page\
                       + (1 if items_count % items_per_page else 0)\
                       or 1

            # Page overflow?
            if page > page_total:
                response = False, {}
            else:
                if items_all:
                    if order_by == 'popular':
                        items = _class.popular(items_all, page, start, end)
                    else:
                        if order_by:
                            filtered = items_all.order_by(order_by)[start:end]
                        else:
                            filtered = items_all[start:end]

                        # Generate item data
                        for item in filtered:
                            items.append(_class._generate_data(item))

                response = True, {
                    'items': items,
                    'explore_page': page,
                    'explore_page_total': page_total,
                }

            CacheHelper.io.set(namespace, response, 300)

        return response


class TutorialsExploreHelper(BaseExploreHelper):
    """
    An helper on explore (tutorials) operations
    """

    @staticmethod
    def _read_items(*args, **kwargs):
        """
        Read tutorial items
        """
        author_id = kwargs.get('author_id', None)
        tutorials_all = TutorialMeta.objects.filter(is_online=True, status=StatusesHelper.encode('accepted'))

        if author_id:
            my_tutorials = [t.tutorial_id for t in TutorialAuthor.objects.filter(user_id=author_id)]
            tutorials_all = tutorials_all.filter(id__in=my_tutorials)

        return tutorials_all


    @staticmethod
    def _generate_data(tutorial):
        """
        Generate tutorial data
        """
        return TutorialProcessHelper.generate_data(tutorial)


    @classmethod
    def _popular_process(_class, tutorials_all):
        """
        Process popularity data (take shares into account)
        """
        processed = super(TutorialsExploreHelper, _class)._popular_process(tutorials_all)

        for tutorial in processed:
            tutorial['popularity'] += (5 * tutorial['meta'].shares)

        return processed


    @classmethod
    def build_response(_class, request, page=1, order_by=None, author_id=None):
        """
        Builds the tutorials explore response data
        """
        namespace = CacheHelper.ns('explore:helpers:tutorials:build_response', page=page, order_by=order_by, author_id=author_id)

        return super(TutorialsExploreHelper, _class).build_response(
            namespace=namespace,
            request=request,
            items_per_page=10,
            page=page,
            order_by=order_by,
            author_id=author_id,
        )


    @classmethod
    def popular(_class, tutorials_all, page, start, end):
        """
        Returns the tutorials sorted by popularity according to the page
        """
        namespace = CacheHelper.ns('explore:helpers:tutorials:popular')

        return super(TutorialsExploreHelper, _class)._popular_data(namespace, tutorials_all, page, start, end)


class BooksExploreHelper(BaseExploreHelper):
    """
    An helper on explore (books) operations
    """

    @staticmethod
    def _read_items(*args, **kwargs):
        """
        Read book items
        """
        return BookHelper.list()


    @staticmethod
    def _generate_data(book):
        """
        Generate book data
        """
        return BookHelper.generate_data(book)


    @classmethod
    def build_response(_class, request, page=1, order_by=None):
        """
        Builds the books explore response data
        """
        namespace = CacheHelper.ns('explore:helpers:books:build_response', page=page, order_by=order_by)

        return super(BooksExploreHelper, _class).build_response(
            namespace=namespace,
            request=request,
            items_per_page=10,
            page=page,
            order_by=order_by,
        )


    @classmethod
    def popular(_class, books_all, page, start, end):
        """
        Returns the books sorted by popularity according to the page
        popularity = views + 5 * shares + 5 * relevant - 20 * irrelevant
        """
        namespace = CacheHelper.ns('explore:helpers:books:popular')

        return super(BooksExploreHelper, _class)._popular_data(namespace, books_all, page, start, end)


class SpotsExploreHelper(BaseExploreHelper):
    """
    An helper on explore (spots) operations
    """

    @staticmethod
    def _read_items(*args, **kwargs):
        """
        Read book items
        """
        return SpotHelper.list()


    @staticmethod
    def _generate_data(spot):
        """
        Generate spot data
        """
        return SpotHelper.generate_data(spot)


    @classmethod
    def _popular_process(_class, items_all):
        """
        Process popularity data
        popularity = views
        """
        processed = []

        # Compute the item popularity
        for item in items_all:
            item = _class._generate_data(item)

            item['popularity'] = int(item['views'])
            
            processed.append(item)

        return processed


    @classmethod
    def build_response(_class, request, page=1, order_by=None):
        """
        Builds the spots explore response data
        """
        namespace = CacheHelper.ns('explore:helpers:spots:build_response', page=page, order_by=order_by)

        return super(SpotsExploreHelper, _class).build_response(
            namespace=namespace,
            request=request,
            items_per_page=15,
            page=page,
            order_by=order_by,
        )


    @classmethod
    def popular(_class, spots_all, page, start, end):
        """
        Returns the spots sorted by popularity according to the page
        popularity = views + 5 * shares + 5 * relevant - 20 * irrelevant
        """
        namespace = CacheHelper.ns('explore:helpers:spots:popular')

        return super(SpotsExploreHelper, _class)._popular_data(namespace, spots_all, page, start, end)
