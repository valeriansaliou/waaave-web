from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap

from _commons.helpers.statuses import StatusesHelper

from .models import *


class TutorialSitemap(Sitemap):
    """
    Build the tutorial sitemap
    """
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        results = []
        filtered = Meta.objects.filter(
            is_online=True,
            status__gte=StatusesHelper.encode('accepted'),
        )

        for tutorial in filtered.iterator():
            tutorial_url = tutorial.url_set.filter(is_alias=False).first()

            results.append({
                'tag': tutorial_url.tag,
                'slug': tutorial_url.slug,
                'date': tutorial.date_update,
            })

        return results

    def location(self, obj):
        return reverse('tutorial.views.view', kwargs={
            'tag': obj['tag'],
            'slug': obj['slug'],
        })

    def lastmod(self, obj):
        return obj['date']
