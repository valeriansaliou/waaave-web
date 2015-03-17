from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap

from .helpers import *
from .models import *


class SpotSitemap(Sitemap):
    """
    Build the spot sitemap
    """
    changefreq = 'hourly'
    priority = 0.5

    def items(self):
        results = []

        for spot in SpotHelper.list():
            results.append({
                'tag': spot.slug,
                'date': spot.date,
            })

        return results

    def location(self, obj):
        return reverse('spot.views.view_root', kwargs={
            'tag': obj['tag'],
        })

    def lastmod(self, obj):
        return obj['date']
