from django.conf.urls import patterns

urlpatterns = patterns('services.views',
    (r'^$', 'root'),
    (r'^advertise/$', 'advertise'),
    (r'^bootstrap/$', 'bootstrap'),
    (r'^api/$', 'api'),
)