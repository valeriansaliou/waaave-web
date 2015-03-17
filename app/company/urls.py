from django.conf.urls import patterns

urlpatterns = patterns('company.views',
    (r'^$', 'root'),
    (r'^about/$', 'about'),
    (r'^terms/$', 'terms'),
    (r'^privacy/$', 'privacy'),
    (r'^contact/$', 'contact'),
)