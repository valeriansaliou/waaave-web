from django.conf.urls import patterns

urlpatterns = patterns('newsletter.views',
    (r'^$', 'root'),
)