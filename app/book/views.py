from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect, Http404
from django.core.urlresolvers import reverse

from _commons.helpers.cache import CacheHelper

from .helpers import *


def root(request):
    """
    Book > Root
    """
    return HttpResponsePermanentRedirect(reverse('explore.views.books'))


def view(request, author, slug):
    """
    Book > View
    """
    namespace = CacheHelper.ns('book:views:view', author=author, slug=slug)
    response_data = CacheHelper.io.get(namespace)

    if not response_data:
        # Get book data
        book, status, path = BookHelper.check('view', author, slug)

        # Check book actions
        if status in ('not_found', 'not_visible'):
            raise Http404
        elif status == 'redirect':
            return HttpResponsePermanentRedirect(path)

        data = BookHelper.generate_data(book)

        response_data = {
            'book': data,

            'item_type': 'book',
            'item_id': book.id,
        }

        CacheHelper.io.set(namespace, response_data)

    return render(request, 'book/book_view.jade', response_data)


def view_relevance(request, author, slug):
    """
    Book > Relevance
    """
    pass
