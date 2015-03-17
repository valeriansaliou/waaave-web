from django.db import models
from bbcode.fields import BBCodeTextField

from _commons.helpers.languages import LanguagesHelper
from _commons.models import DatedAbstract, TagAbstract
from _commons.fields import ISBNField, LanguageField

from .settings import *
from .helpers import *


# Meta: stores meta data about books
class Item(DatedAbstract):
    """
    Database [book.meta]
    """
    title = models.CharField(db_index=True, blank=False, max_length=BOOK_TITLE_MAX)
    description = BBCodeTextField(blank=False)

    pages = models.PositiveIntegerField(default=0)
    isbn = ISBNField()
    language = LanguageField(default='en')

    cover_original = models.FileField(upload_to=BookHelper.get_cover_path_original)
    cover_small = models.FileField(upload_to=BookHelper.get_cover_path_small)
    cover_medium = models.FileField(upload_to=BookHelper.get_cover_path_medium)
    cover_large = models.FileField(upload_to=BookHelper.get_cover_path_large)

    is_visible = models.BooleanField(db_index=True, default=False)
    amazon_id = models.CharField(max_length=10)

    date_release = models.DateTimeField()

    def __unicode__(self):
        return u'%s' % (self.title)

    def url_cover_original(self):
        return BookHelper.get_cover_absolute_url(
            self.cover_original or DEFAULT_COVER_PATH['original']
        )

    def url_cover_small(self):
        return BookHelper.get_cover_absolute_url(
            self.cover_small or DEFAULT_COVER_PATH['small']
        )

    def url_cover_medium(self):
        return BookHelper.get_cover_absolute_url(
            self.cover_medium or DEFAULT_COVER_PATH['medium']
        )

    def url_cover_large(self):
        return BookHelper.get_cover_absolute_url(
            self.cover_large or DEFAULT_COVER_PATH['large']
        )

    def language_name(self):
        return LanguagesHelper.get_name_from_iso(self.language) or ''


# Person: defines a book personal entity (a physical person)
class Person(DatedAbstract):
    """
    Database [book.person]
    """
    first_name = models.CharField(blank=False, max_length=255)
    last_name = models.CharField(blank=False, max_length=255)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)


# House: defines a book publishing house entity (an anonymous entity, a company)
class House(DatedAbstract):
    """
    Database [book.house]
    """
    name = models.CharField(blank=False, max_length=255)
    website = models.URLField()

    def __unicode__(self):
        return u'%s' % user.name


# Author: binds an author to its book
class Author(DatedAbstract):
    """
    Database [book.author]
    """
    book = models.OneToOneField(Item)
    person = models.OneToOneField(Person)

    def __unicode__(self):
        return u'%s' % (self.person)


# Publisher: defines a book publisher entity (an anonymous entity, a company)
class Publisher(DatedAbstract):
    """
    Database [book.publisher]
    """
    book = models.OneToOneField(Item)
    house = models.OneToOneField(House)

    def __unicode__(self):
        return u'%s' % (self.house)


# Url: stores URLs of books (with URL change tracking)
class Url(DatedAbstract):
    """
    Database [book.url]
    """
    book = models.ForeignKey(Item)

    author = models.CharField(db_index=True, blank=False, max_length=BOOK_AUTHOR_MAX)
    slug = models.CharField(db_index=True, blank=False, max_length=BOOK_SLUG_MAX)
    is_alias = models.BooleanField(db_index=True, default=False)

    def __unicode__(self):
        return u'%s' % (self.slug)


# Tag: stores tags that are mapped to a given book
class Tag(TagAbstract):
    """
    Database [book.tag]
    """
    book = models.ForeignKey(Item, related_name='book_tags')
