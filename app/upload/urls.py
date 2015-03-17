from django.conf.urls import patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('upload.views',
    (r'^uploader/$', 'uploader'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)