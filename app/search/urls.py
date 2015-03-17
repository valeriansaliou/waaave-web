from django.conf.urls import patterns

urlpatterns = patterns('search.views',
    (r'^$', 'root'),
    (r'^\?p=(?P<page>\d+)$', 'root_page'),
    (r'^suggest/$', 'suggest'),
)