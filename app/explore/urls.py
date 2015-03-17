from django.conf.urls import patterns

urlpatterns = patterns('explore.views',
    (r'^$', 'root'),

    (r'^tutorials/(?:(?P<page>\d+)/)?$', 'tutorials'),
    (r'^tutorials/popular/(?:(?P<page>\d+)/)?$', 'tutorials_popular'),
    (r'^tutorials/alphabetical/(?:(?P<page>\d+)/)?$', 'tutorials_alphabetical'),
    (r'^tutorials/yours/(?:(?P<page>\d+)/)?$', 'tutorials_yours'),

    (r'^books/(?:(?P<page>\d+)/)?$', 'books'),
    (r'^books/popular/(?:(?P<page>\d+)/)?$', 'books_popular'),
    (r'^books/alphabetical/(?:(?P<page>\d+)/)?$', 'books_alphabetical'),

    (r'^spots/(?:(?P<page>\d+)/)?$', 'spots'),
    (r'^spots/popular/(?:(?P<page>\d+)/)?$', 'spots_popular'),
    (r'^spots/alphabetical/(?:(?P<page>\d+)/)?$', 'spots_alphabetical'),
)