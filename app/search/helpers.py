from django.contrib.auth.models import User as AuthUser

from tutorial.helpers.process import ProcessHelper as TutorialProcessHelper
from tutorial.helpers.read import ReadHelper as TutorialReadHelper
from tutorial.models import Meta as TutorialMeta

from book.helpers import BookHelper
from spot.helpers import SpotHelper
from user.helpers import StatsUserHelper as UserStatsUserHelper



class CommonListHelper(object):
    """
    An helper on common list operations
    """

    @staticmethod
    def paging(items_all, results_per_page):
        """
        Process paging values
        """
        items_count = len(items_all) if items_all else 0
        items_pages = items_count // results_per_page\
                    + (1 if items_count % results_per_page else 0)

        return items_count, items_pages



class TutorialsListHelper(object):
    """
    An helper on tutorials list operations
    """

    @staticmethod
    def adapt(tutorials, start, end):
        """
        Additional data for tutorial SERP
        """
        adapted, list_ids = [], []

        for tutorial in tutorials[start:end]:
            if tutorial:
                list_ids.append(tutorial.meta_id)

        filtered = TutorialMeta.objects.filter(id__in=list_ids)

        for meta in filtered:
            adapted.append(
                TutorialProcessHelper.generate_data(meta)
            )

        return adapted


class BooksListHelper(object):
    """
    An helper on books list operations
    """

    @staticmethod
    def adapt(books, start, end):
        """
        Additional data for tutorial SERP
        """
        adapted, list_ids = [], []

        for book in books[start:end]:
            if book:
                list_ids.append(book.item_id)

        for meta in BookHelper.list().filter(id__in=list_ids):
            adapted.append(
                BookHelper.generate_data(meta)
            )

        return adapted


class SpotsListHelper(object):
    """
    An helper on spots list operations
    """

    @staticmethod
    def adapt(spots, start, end):
        """
        Additional data for tutorial SERP
        """
        adapted, list_ids = [], []

        for spot in spots[start:end]:
            if spot:
                list_ids.append(spot.item_id)

        for meta in SpotHelper.list().filter(id__in=list_ids):
            adapted.append(
                SpotHelper.generate_data(meta)
            )

        return adapted


class UsersListHelper(object):
    """
    An helper on users list operations
    """

    @staticmethod
    def adapt(users, start, end):
        """
        Additional data for user SERP
        """
        adapted, list_ids = [], []

        for user in users[start:end]:
            if user:
                list_ids.append(user.user_id)

        filtered = AuthUser.objects.filter(id__in=list_ids)

        for user in filtered:
            adapted.append({
                'user': user,
                'profile': user.profile,
                'stats': UserStatsUserHelper(user).get(),
                'tutorial': (TutorialReadHelper.random_for_author(user) + [None])[0],
            })

        return adapted
