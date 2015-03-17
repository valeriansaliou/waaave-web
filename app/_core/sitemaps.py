from user.sitemap import *
from tutorial.sitemap import *
from book.sitemap import *
from spot.sitemap import *


def sitemaps():
    """
    List the sitemap items
    """
    return {
        'user': UserSitemap,
        'tutorial': TutorialSitemap,
        'book': BookSitemap,
        'spot': SpotSitemap,
    }