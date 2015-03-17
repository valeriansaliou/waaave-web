from django.conf.urls import patterns

urlpatterns = patterns('blog.views',
    (r'^(?:page/(?P<page_number>\d+)/)?$', 'page'),
    (r'^date/((?P<date_year>\d{4})/((?P<date_month>\d{2})/((?P<date_day>\d{2})/)?)?)?$', 'date'),
    (r'^category/(?P<category_slug>[^\/]+)/$', 'category'),
    (r'^post/(?P<post_year>\d{4})/(?P<post_slug>[^\/]+)/$', 'post'),
)