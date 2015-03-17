from django.conf.urls import patterns, include
from robots.utils import url

urlpatterns = patterns('account.views',
    url(r'^login/$', 'login_root', robots_allow=False),
    (r'^logout/$', 'logout_root'),

    (r'^register/$', 'register_root'),
    url(r'^register/go/$', 'register_go', robots_allow=False),
    url(r'^register/profile/$', 'register_profile', robots_allow=False),
    url(r'^register/about/$', 'register_about', robots_allow=False),
    url(r'^register/done/$', 'register_done', robots_allow=False),

    (r'^recover/$', 'recover_root'),
    url(r'^recover/(?P<uidb36>[0-9A-Za-z]{3})-(?P<token>[0-9A-Za-z]{20})-(?P<random>[0-9A-Za-z]{40})/$', 'recover_key', robots_allow=False),
    url(r'^recover/proceed/$', 'recover_proceed', robots_allow=False),

    url(r'^confirm/(?P<uidb36>[0-9A-Za-z]{3})-(?P<token>[0-9A-Za-z]{20})-(?P<random>[0-9A-Za-z]{40})/$', 'confirm_key', robots_allow=False),
    url(r'^confirm/retry/(?:\?next=(.*))?$', 'confirm_retry', robots_allow=False),

    url(r'^settings/$', 'settings_root', robots_allow=False),
    url(r'^settings/credentials/$', 'settings_credentials', robots_allow=False),
    url(r'^settings/notifications/$', 'settings_notifications', robots_allow=False),
    url(r'^settings/notifications/fetch/(?P<page>\d+)/$', 'settings_notifications_fetch', robots_allow=False),
    url(r'^settings/ajax/avatar/$', 'settings_ajax_avatar', robots_allow=False),
)

urlpatterns += patterns('',
    url(r'^login/(?P<backend>[^/]+)/$', 'account.views.login_social', robots_allow=False),
    url(r'^complete/(?P<backend>[^/]+)/$', 'account.views.complete_social', robots_allow=False),
    url(r'^disconnect/(?P<backend>[^/]+)/$', 'account.views.disconnect_social', robots_allow=False),
    (r'', include('social.apps.django_app.urls', namespace='social')),
)