from django.conf.urls import patterns, url, include
from tour_config import views

urlpatterns = patterns('',
                       url(r'^tour_config/(?P<pk>\d+)/$',
                           views.GetTourConfig.as_view()),
                       url(r'^tour_config/(?P<tour_id>.+)/$',
                           views.GetTourConfig.as_view()),
                       )
