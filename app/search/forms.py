from haystack.forms import SearchForm
from django.contrib.auth.models import User as AuthUser

from _commons.helpers.strings import StringsHelper

from tutorial.models import Meta as TutorialMeta
from book.models import Item as BookItem
from tag.models import List as TagList


class TyphoonSearchForm(SearchForm):
    """
    Search form
    """

    def __filter_models(self, results, model):
        """
        Filter the search query results with given model (exclude other model instances)
        """
        filtered = []

        for result in results:
            if isinstance(result.object, model):
                filtered.append(result)

        return filtered


    def clean_q(self):
        """
        Normalize the search query
        """
        return StringsHelper.strip_accents(
            self.cleaned_data.get('q')
        )


    def search_tutorials(self):
        """
        Return all tutorials
        """
        sqs = super(TyphoonSearchForm, self).search()
        sqs = sqs.models(TutorialMeta)

        return self.__filter_models(sqs, TutorialMeta)


    def search_books(self):
        """
        Return all books
        """
        sqs = super(TyphoonSearchForm, self).search()
        sqs = sqs.models(BookItem)

        return self.__filter_models(sqs, BookItem)


    def search_spots(self):
        """
        Return all spots
        """
        sqs = super(TyphoonSearchForm, self).search()
        sqs = sqs.models(TagList)

        return self.__filter_models(sqs, TagList)


    def search_users(self):
        """
        Return all users
        """
        sqs = super(TyphoonSearchForm, self).search()
        sqs = sqs.models(AuthUser)

        return self.__filter_models(sqs, AuthUser)
