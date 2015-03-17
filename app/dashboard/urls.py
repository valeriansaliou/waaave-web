from django.conf.urls import patterns

urlpatterns = patterns('dashboard.views',
    (r'^$', 'root'),
    (r'^shots/$', 'shot_root'),
    (r'^shot/new/$', 'shot_new'),
    (r'^shot/edit/(?P<shot_id>\d+)/$', 'shot_edit'),
    (r'^tutorials/$', 'tutorial_root'),
    (r'^tutorial/new/$', 'tutorial_new'),
    (r'^tutorial/edit/(?P<tutorial_id>\d+)/$', 'tutorial_edit'),
    (r'^tutorial/trash/$', 'tutorial_trash'),
    (r'^followings/$', 'followings'),
    (r'^profile/settings/$', 'profile_settings'),
)