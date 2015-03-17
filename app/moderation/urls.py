from django.conf.urls import patterns

urlpatterns = patterns('moderation.views',
    (r'^$', 'root'),
    (r'^tutorials/$', 'tutorials'),
    (r'^tutorial/trash/$', 'tutorial_trash'),
    (r'^shots/$', 'shots'),
    (r'^comments/$', 'comments'),
    (r'^comments/(?P<page>\d+)/$', 'comments'),
    (r'^users/$', 'users'),
    (r'^advertising/$', 'advertising'),
)