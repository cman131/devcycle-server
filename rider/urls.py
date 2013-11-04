from django.conf.urls import patterns, url
from rider import views

urlpatterns = patterns('',
                       # register rider
                       url(r'^register/$',
                           views.RiderAPI.as_view()),
                       # register riders push ID
                       url(r'^register_push/$',
                           views.RiderPushUpdateAPI.as_view()),
                       )
