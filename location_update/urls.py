from django.conf.urls import patterns, url
from location_update import views

urlpatterns = patterns('',
                       url(r'^location_update/$',
                           views.LocationAPI.as_view()),
                       url(r'^route/$',
                           views.RouteAPI.as_view()),
                        url(r'^playback/frames/$',
                           views.PlaybackAPI.as_view()),
                      )

# Unused code removed - EM 2/13/13
#                       url(r'^location_update2/$',
#                           views.Location2API.as_view())
