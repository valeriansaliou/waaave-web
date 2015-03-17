from django.conf.urls import patterns

urlpatterns = patterns('home.views',
    (r'^$', 'root'),
)
