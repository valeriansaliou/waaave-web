from django.conf.urls import patterns

urlpatterns = patterns('activity.views',
    (r'^$', 'root'),
    (r'^statistics/$', 'statistics'),
    (r'^comments/$', 'comments'),
)