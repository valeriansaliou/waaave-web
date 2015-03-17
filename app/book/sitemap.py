from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap

from .helpers import *
from .models import *


class BookSitemap(Sitemap):
    """
    Build the book sitemap
    """
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        results = []

        for book in BookHelper.list():
            book_url = BookHelper.url(book)

            results.append({
                'author': book_url.author,
                'slug': book_url.slug,
                'date': book.date_update,
            })

        return results

    def location(self, obj):
        return reverse('book.views.view', kwargs={
            'author': obj['author'],
            'slug': obj['slug'],
        })

    def lastmod(self, obj):
        return obj['date']
