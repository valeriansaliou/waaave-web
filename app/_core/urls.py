from django.conf.urls import patterns, include
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse

from hitcount.views import update_hit_count_ajax
from robots.utils import url
from _core.sitemaps import sitemaps


# Primary URLs
urlpatterns = patterns('',
    ## Important: order the rules from most accessed to less accessed
    ##            thus, to ensure the best performance as Django stops on first matching rule
    ## Plus: some URLs are buggy if not defined first, hence this apart URL definition

    # Hitcount url to save hits on entity
    url(r'^ajax/hit/$', update_hit_count_ajax, name='hitcount_update_ajax'),
)


# Main URLs
urlpatterns += patterns('',
    # Most visited pages
    (r'^$', include('home.urls')),
    (r'^avatar/', include('avatar.urls')),
    (r'^api/', include('api.urls')),
    (r'^shot/', include('shot.urls')),
    (r'^tutorial/', include('tutorial.urls')),
    (r'^user/', include('user.urls')),
    (r'^search/', include('search.urls')),
    (r'^timeline/', include('timeline.urls')),
    (r'^spot/', include('spot.urls')),
    (r'^book/', include('book.urls')),
    (r'^comment/', include('comment.urls')),
    (r'^relevance/', include('relevance.urls')),
    (r'^share/', include('share.urls')),

    # Less visited pages
    (r'^blog/', include('blog.urls')),
    (r'^account/', include('account.urls')),
    (r'^notification/', include('notification.urls')),
    (r'^activity/', include('activity.urls')),
    (r'^applications/', include('applications.urls')),
    (r'^company/', include('company.urls')),
    (r'^dashboard/', include('dashboard.urls')),
    (r'^explore/', include('explore.urls')),
    (r'^feedback/', include('feedback.urls')),
    (r'^moderation/', include('moderation.urls')),
    (r'^newsletter/', include('newsletter.urls')),
    (r'^services/', include('services.urls')),
    (r'^upload/', include('upload.urls')),
    (r'^pro/', include('pro.urls')),
)


# Aliases (redirects)
urlpatterns += patterns('',
    (r'^(login|signin)/$', RedirectView.as_view(url=reverse('account.views.login_root'))),
    (r'^(logout|signout)/$', RedirectView.as_view(url=reverse('account.views.logout_root'))),
    (r'^(register|signup)/$', RedirectView.as_view(url=reverse('account.views.register_root'))),
    (r'^(settings|preferences|parameters)/$', RedirectView.as_view(url=reverse('account.views.settings_root'))),
    (r'^(home|timeline)/$', RedirectView.as_view(url=reverse('home.views.root'))),
    (r'^news/$', RedirectView.as_view(url=reverse('blog.views.page'))),
    (r'^tutorials/$', RedirectView.as_view(url=reverse('tutorial.views.root'))),
    (r'^shots/$', RedirectView.as_view(url=reverse('shot.views.root'))),
    (r'^spots/$', RedirectView.as_view(url=reverse('spot.views.root'))),
    (r'^books/$', RedirectView.as_view(url=reverse('book.views.root'))),
    (r'^me/', 'user.views.me'),
)


# Various (apps, ...)
urlpatterns += patterns('',
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps()}),
    (r'^robots.txt$', 'robots.views.robots_txt', {'template': '_core/robots.txt'}),
    (r'^humans.txt$', 'humans.views.humans_txt', {'template': '_core/humans.txt'}),
)

# Error URLs
handler400 = '_commons.views.bad_request_400'
handler403 = '_commons.views.forbidden_403'
handler404 = '_commons.views.not_found_404'
handler500 = '_commons.views.server_error_500'
