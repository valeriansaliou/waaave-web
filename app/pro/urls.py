from django.conf.urls import patterns

urlpatterns = patterns('pro.views',
    (r'^$', 'root'),
)