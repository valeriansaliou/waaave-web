from django.conf.urls import patterns

urlpatterns = patterns('avatar.views',
    (r'^$', 'view'),
    (r'^(?P<username>[^\/]+)(?:/(?P<size>small|normal|large))?/?', 'view'),
)