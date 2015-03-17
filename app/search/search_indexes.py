from haystack import indexes
from bbcode.templatetags.bbcode import bbcode_filter_as_text

from django.contrib.auth.models import User as AuthUser

from tutorial.models import Meta as TutorialMeta
from book.models import Item as BookItem
from tag.models import List as TagList

from _commons.helpers.strings import StringsHelper
from _commons.helpers.statuses import StatusesHelper



class TutorialIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Index the tutorials
    """

    # Searched document
    text = indexes.CharField(document=True)

    # Indexed fields
    meta_id = indexes.IntegerField(model_attr='id')
    meta_title = indexes.CharField(model_attr='title', boost=1.5)
    content_body = indexes.CharField(boost=0.30)

    author_first_name = indexes.CharField(boost=0.5)
    author_last_name = indexes.CharField(boost=0.5)


    def __get_instance_author(self, instance):
        """
        Return the author instance attached to current instance
        """
        return instance.author_set.filter(is_master=True).first()


    def __get_instance_content(self, instance):
        """
        Return the content instance attached to current instance
        """
        return instance.content


    def get_model(self):
        """
        Return the current model
        """
        return TutorialMeta


    def get_updated_field(self):
        """
        Return the update date tracking field
        """
        return 'date_update'


    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated
        """
        return self.get_model().objects.filter(is_online=True, status=StatusesHelper.encode('accepted'))


    def prepare(self, object):
        """
        Prepare the search data
        """
        self.prepared_data = super(TutorialIndex, self).prepare(object)

        return self.prepared_data


    def prepare_meta_title(self, instance):
        """
        Prepare the title field [meta.title]
        """
        return StringsHelper.strip_accents(instance.title)


    def prepare_content_body(self, instance):
        """
        Prepare the title field [meta.content.body]
        """
        return StringsHelper.strip_accents(
            bbcode_filter_as_text(self.__get_instance_content(instance).body)
        )


    def prepare_author_first_name(self, instance):
        """
        Prepare the author first name field [meta.author_set[is_master].user.first_name]
        """
        return StringsHelper.strip_accents(
            self.__get_instance_author(instance).user.first_name
        )


    def prepare_author_last_name(self, instance):
        """
        Prepare the author last name field [meta.author_set[is_master].user.last_name]
        """
        return StringsHelper.strip_accents(
            self.__get_instance_author(instance).user.last_name
        )


    def prepare_text(self, instance):
        """
        Prepare the text document field
        """
        return u'{0}\n{1}\n{2}\n{3}'.format(
            self.prepare_meta_title(instance),
            self.prepare_content_body(instance),
            self.prepare_author_first_name(instance),
            self.prepare_author_last_name(instance),
        )


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Index the books
    """

    # Searched document
    text = indexes.CharField(document=True)

    # Indexed fields
    item_id = indexes.IntegerField(model_attr='id')
    item_title = indexes.CharField(model_attr='title', boost=1.5)
    item_description = indexes.CharField(model_attr='description', boost=0.30)

    author_first_name = indexes.CharField(boost=0.5)
    author_last_name = indexes.CharField(boost=0.5)


    def get_model(self):
        """
        Return the current model
        """
        return BookItem


    def get_updated_field(self):
        """
        Return the update date tracking field
        """
        return 'date_update'


    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated
        """
        return self.get_model().objects.filter(is_visible=True)


    def prepare(self, object):
        """
        Prepare the search data
        """
        self.prepared_data = super(BookIndex, self).prepare(object)

        return self.prepared_data


    def prepare_item_title(self, instance):
        """
        Prepare the title field [item.title]
        """
        return StringsHelper.strip_accents(
            instance.title
        )


    def prepare_item_description(self, instance):
        """
        Prepare the title field [item.description]
        """
        return StringsHelper.strip_accents(
            bbcode_filter_as_text(instance.description)
        )


    def prepare_author_first_name(self, instance):
        """
        Prepare the author first name field [item.author.person.first_name]
        """
        return StringsHelper.strip_accents(
            instance.author.person.first_name
        )


    def prepare_author_last_name(self, instance):
        """
        Prepare the author last name field [item.author.person.last_name]
        """
        return StringsHelper.strip_accents(
            instance.author.person.last_name
        )


    def prepare_text(self, instance):
        """
        Prepare the text document field
        """
        return u'{0}\n{1}\n{2}\n{3}'.format(
            self.prepare_item_title(instance),
            self.prepare_item_description(instance),
            self.prepare_author_first_name(instance),
            self.prepare_author_last_name(instance),
        )


class SpotIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Index the spots
    """

    # Searched document
    text = indexes.CharField(document=True)

    # Indexed fields
    item_id = indexes.IntegerField(model_attr='id')
    item_name = indexes.CharField(model_attr='name', boost=2)
    item_slug = indexes.CharField(model_attr='slug', boost=1.5)
    item_description = indexes.CharField(model_attr='description', boost=0.30)


    def get_model(self):
        """
        Return the current model
        """
        return TagList


    def get_updated_field(self):
        """
        Return the update date tracking field
        """
        return 'date'


    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated
        """
        return self.get_model().objects.all()


    def prepare(self, object):
        """
        Prepare the search data
        """
        self.prepared_data = super(SpotIndex, self).prepare(object)

        return self.prepared_data


    def prepare_item_name(self, instance):
        """
        Prepare the name field [item.name]
        """
        return StringsHelper.strip_accents(
            instance.name
        )


    def prepare_item_slug(self, instance):
        """
        Prepare the slug field [item.slug]
        """
        return StringsHelper.strip_accents(
            instance.slug
        )


    def prepare_item_description(self, instance):
        """
        Prepare the title field [item.description]
        """
        return StringsHelper.strip_accents(
            instance.description
        )


    def prepare_text(self, instance):
        """
        Prepare the text document field
        """
        return u'{0}\n{1}\n{2}'.format(
            self.prepare_item_name(instance),
            self.prepare_item_slug(instance),
            self.prepare_item_description(instance),
        )


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Index the users
    """

    # Searched document
    text = indexes.CharField(document=True)

    # Indexed fields
    user_id = indexes.IntegerField(model_attr='id')

    user_first_name = indexes.CharField(boost=1.25)
    user_last_name = indexes.CharField(boost=1.5)


    def get_model(self):
        """
        Return the current model
        """
        return AuthUser


    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.all()


    def prepare_user_first_name(self, instance):
        """
        Prepare the first name field [user.first_name]
        """
        return StringsHelper.strip_accents(
            instance.first_name
        )


    def prepare_user_last_name(self, instance):
        """
        Prepare the last name field [user.last_name]
        """
        return StringsHelper.strip_accents(
            instance.last_name
        )


    def prepare_text(self, instance):
        """
        Prepare the text document field
        """
        return u'{0}\n{1}'.format(
            self.prepare_user_first_name(instance),
            self.prepare_user_last_name(instance),
        )
