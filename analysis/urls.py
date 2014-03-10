from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required
from tour_config.views import TourConfigUpdate, TourConfigAdd, ServerPollRateUpdate
from analysis import views
from sites import tt_admin
from django.views.generic import ListView
from tour_config.models import TourRoute
from tour_config.admin import TourRouteAdmin

urlpatterns = patterns('',
                       url(r'^login/$',
                           'django.contrib.auth.views.login',
                           {'template_name': 'login.html'},
                           name='login'),
                       url(r'^$',
                           views.home_view),
                       url(r'^home/$',
                           views.home_view,
                           name='home'),
                       url(r'^server/pollingrate/update/$',
                            login_required(
                              ServerPollRateUpdate.as_view()
                            ),
                           name='server-polling-rate-update'
                           ),
                       url(r'^graphs/$',
                           views.graph_view_os,
                           name='graphs'),
                       url(r'^graphs/os/$',
                           views.graph_view_os,
                           name='graphs-os'),
                       url(r'^graphs/registered/$',
                           views.graph_view_registered,
                           name='graphs-registered'),
                       url(r'^graphs/updates/$',
                           views.graph_view_updates,
                           name='graphs-updates'),
                       url(r'^graphs/battery/$',
                           views.graph_view_battery,
                           name='graphs-battery'),
                       url(r'^gcm/$',
                           login_required(TourConfigUpdate.as_view()),
                           name='gcm'),
                       url(r'^send_message/$',
                           views.send_message_view,
                           name='send_message'),
                       url(r'^map/$',
                           views.map_view,
                           name='map'),
                       url(r'^playback/$',
                           views.playback_view,
                           name='playback'),
                       url(r'^tourroutes/$', ListView.as_view(
                                             model=TourRoute,
                                             context_object_name='tourroute_list',
                                             template_name='tourroute_list.html'
                                             )),
                       url(r'^tourconfig/add/$',
                           login_required(TourConfigAdd.as_view()),
                           name='tourconfig-add'),
                       url(r'^logout/$',
                           views.logout_view,
                           name='logout'),
                       (r'^admin/',
                           include(tt_admin.urls)),
                       )
