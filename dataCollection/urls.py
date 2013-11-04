import settings
from django.conf.urls import *

urlpatterns = patterns('',
                       url(r'^', include('rider.urls')),
                       url(r'^', include('location_update.urls')),
                       url(r'^', include('tour_config.urls')),
                       url(r'^', include('analysis.urls')),
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': settings.MEDIA_ROOT}),
                       )

