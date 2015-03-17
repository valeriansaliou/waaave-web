from django.conf.urls import patterns

urlpatterns = patterns('applications.views',
    (r'^$', 'root'),
    (r'^ios/$', 'ios'),
    (r'^android/$', 'android'),
)