from django.conf.urls import patterns

urlpatterns = patterns('shot.views',
    (r'^$', 'root'),
    (r'^(?P<tag>[\w-]+)/$', 'tag'),
    (r'^(?P<tag>[\w-]+)/(?P<slug>[\w-]+)/$', 'view'),
)