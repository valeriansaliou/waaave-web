from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap

from django.contrib.auth.models import User as AuthUser


class UserSitemap(Sitemap):
    """
    Build the user sitemap
    """
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        results = []

        for cur_user in AuthUser.objects.iterator():
            results.append({
                'username': cur_user.username,
                'date': cur_user.profile.date_update,
            })

        return results

    def location(self, obj):
        return reverse('user.views.main', kwargs={
            'username': obj['username']
        })

    def lastmod(self, obj):
        return obj['date']
