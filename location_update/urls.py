from django.conf.urls import patterns, url
from location_update import views

urlpatterns = patterns('',
                       url(r'^location_update/$',
                           views.LocationAPI.as_view()),
                       url(r'^location_update/recent/$',
                           views.RecentLocationAPI.as_view()),
                       url(r'^route/$',
                           views.RouteAPI.as_view()),
                        url(r'^playback/frames/$',
                           views.PlaybackAPI.as_view()),
			url(r'^get_location_data/(?P<aff_id>\w{3,7})/$',
			   views.get_location_data_view)
                      )

# Unused code removed - EM 2/13/13
#                       url(r'^location_update2/$',
#                           views.Location2API.as_view())
