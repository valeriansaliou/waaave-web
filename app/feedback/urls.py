from django.conf.urls import patterns

urlpatterns = patterns('feedback.views',
    (r'^$', 'root'),
)