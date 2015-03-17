from django.conf.urls import patterns
from robots.utils import url

urlpatterns = patterns('timeline.views',
    url(r'^fetch/(?P<fetch_filter>following|followers|everyone)/(?P<page>\d+)/$', 'fetch', robots_allow=False),
	(r'^followers/$', 'followers'),
    (r'^everyone/$', 'everyone'),
)