from django.conf.urls import patterns

urlpatterns = patterns('api.views',
    (r'^$', 'root'),
    (r'^user/session/$', 'user_session'),
)
