from django.conf.urls import patterns, url
from rider import views

urlpatterns = patterns('',
						# register rider
						url(r'^register/$',
							views.RiderAPI.as_view()),
						# register riders push ID
						url(r'^register_push/$',
							views.RiderPushUpdateAPI.as_view()),
						# get affinity group data
						url(r'^list_group/(?P<r_id>\w+)/$', 
							views.list_group_view),
						# create an affinity group
						url(r'^create_group/$',
							views.create_group_view),
						# join an affinity group
						url(r'^join_group/(?P<aff_id>\w{3,7})/(?P<r_id>\w+)/$',
							views.join_group_view),
						# leave an affinity group
						url(r'^leave_group/(?P<aff_id>\w{3,7})/(?P<r_id>\w+)/$',
							views.leave_group_view),
						# check code validity
						url(r'^check_code/(?P<aff_id>\w{3,7})/$',
							views.check_code_view)
						)
