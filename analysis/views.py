from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from forms import LoginForm, SendMessageForm
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from location_update.utils import get_update_data, get_battery_info, get_location_updates
from rider.utils import get_os_data, get_registration_data, get_num_registered
from django.contrib import messages
from rider.models import Rider
from tour_config.models import TourConfig
from location_update.models import Location
from django.conf import settings
from urllib2 import urlopen, Request, URLError, HTTPError
from django.db.models import Count
import time
import json
import urllib
from datetime import timedelta, date, timedelta, tzinfo
import datetime
import calendar

ZERO = timedelta(0)

# A UTC class.

class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

@ensure_csrf_cookie
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usr = form.cleaned_data
            user = authenticate(username=usr['user'], password=usr['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)

                    return render_to_response(
                        'home.html',
                        {},
                        context_instance=RequestContext(request))

            # Redirect to a success page.
                else:
                    raise Http404("Your account has been disabled!")
            else:
                raise Http404("Your username and password were incorrect.")
    else:
        form = LoginForm()
        return render_to_response(
            'login.html',
            {'form': form},
            context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return redirect('login')

@requires_csrf_token
@login_required(login_url='/login/')
def home_view(request):
    data = {}
    try:
        current_tour = TourConfig.objects.values('tour_id', 'tour_name', 'start_time', 'max_tour_time', 'tour_organization', 'tour_logo', 'dcs_url', 'server_polling_rate', 'location_polling_rate').latest('pk')
    except TourConfig.DoesNotExist:
        current_tour = False

    if current_tour:
        current_stats = {}
        current_stats['riders'] = Rider.objects.count()

	   #current_time = datetime.datetime.utcnow()
	   #current_time = current_time.replace(tzinfo=UTC())
        if time.time() > current_tour['start_time']:
            pass
            #current_stats['total_updates'] = Location.objects.filter(tour_id=current_tour['tour_id']).count()
            #current_stats['active_riders'] = Rider.objects.annotate(location_count=Count('location_update')).filter(location_count__gt=1).count()
        data['current_stats'] = current_stats
        current_tour['start_time'] = datetime.datetime.fromtimestamp(current_tour['start_time'])
        current_tour['max_tour_time'] =datetime.datetime.fromtimestamp(current_tour['max_tour_time'])
        current_tour['config_link'] = "tourtrak://?" + urllib.urlencode({'tour_id': current_tour['tour_id'], 'dcs_url': current_tour['dcs_url'], 'tour_name': current_tour['tour_name']})
        data['current_tour'] = current_tour
    return render_to_response('home.html',data, context_instance=RequestContext(request))

@requires_csrf_token
@login_required(login_url='/login/')
def graph_view(request):
    data = {}
    data.update(get_num_registered())
    data.update(get_location_updates())
    return render_to_response('graph.html',data, context_instance=RequestContext(request))

@requires_csrf_token
@login_required(login_url='/login/')
def graph_view_os(request):
    data = get_os_data()
    data['title'] = "User Operating System Breakdown"
    return render_to_response('graph_pie.html',data, context_instance=RequestContext(request))

@requires_csrf_token
@login_required(login_url='/login/')
def graph_view_registered(request):
    data = get_registration_data()
    data['title'] = "Rider Registration by day"
    return render_to_response('graph_line.html',data, context_instance=RequestContext(request))

@requires_csrf_token
@login_required(login_url='/login/')
def graph_view_updates(request):
    data = get_update_data()
    data['title'] = "Locations Updates Over Time"
    return render_to_response('graph_line.html',data, context_instance=RequestContext(request))

@requires_csrf_token
@login_required(login_url='/login/')
def graph_view_battery(request):
    data = get_battery_info()
    data['title'] = "Average Rider Battery Life Over Time"
    return render_to_response('graph_line.html',data, context_instance=RequestContext(request))

#MAPPING
@requires_csrf_token
@login_required(login_url='/login/')
def map_view(request):
    """
    Start with the default center from settings.py
    If there's a tour route associated with the current tour, center
    on that instead. If not, see if there are any locations in the database
    and center on the most recent one.
    """
    center = ( settings.DEFAULT_MAP_LON, settings.DEFAULT_MAP_LAT )
    try:
        tour = TourConfig.objects.latest('pk')
    except ObjectDoesNotExist as e:
        tour = None
    if tour is not None and tour.tour_route is not None:
        center = tour.tour_route.route.centroid.coords
    elif Location.objects.count() > 0:
        location = Location.objects.latest('pk')
        center = location.coords.coords
    return render_to_response('map.html', {'ext_tmp':'map_base.html', 'center': center, 'map_tile_server': settings.MAP_TILE_SERVER}, context_instance=RequestContext(request))


@requires_csrf_token
@login_required(login_url='/login/')
def playback_view(request):
    tour = TourConfig.objects.latest('pk')
    if tour is not None and tour.tour_route is not None:
        center = tour.tour_route.route.centroid.coords
    else:
        center = ( settings.DEFAULT_MAP_LON, settings.DEFAULT_MAP_LAT )
    return render_to_response('playback.html', { 'map_tile_server': settings.MAP_TILE_SERVER, 'center': center }, context_instance=RequestContext(request))

@requires_csrf_token
@login_required(login_url='/login/')
def send_message_view(request):
    if(request.method == "POST"):
        form = SendMessageForm(request.POST)

        if(form.is_valid()):
            push_ids = []
            for rider in Rider.objects.iterator():
                if rider.push_id is not None and len(rider.push_id) > 0:
                    push_ids.append(rider.push_id)

            if len(push_ids) > 0:
                headers = {}
                headers[settings.GCM_API_KEY_HEADER] = 'key='+settings.GCM_API_KEY
                headers['Content-Type'] = 'application/json'
                data = {}
                data['registration_ids'] = push_ids
                data['data'] = {}
                data['data']['msg'] = form.cleaned_data['message'] # For legacy sake (last sr project)
		data['data']['message'] = form.cleaned_data['message']

                req = Request(settings.GCM_SEND_URL, json.dumps(data), headers)
                urlopen(req)
                messages.success(request, 'Message was sent successfully.')
            else:
                messages.info(request, 'No riders to message.')
    else:
        form = SendMessageForm()

    return render(request, 'send_message.html', {'form': form})

#GCM
@requires_csrf_token
@login_required(login_url='/login/')
def gcm_config_view(request):
    data = {}
    data['title'] = 'Change Tour Information'
    return render_to_response('gcm.html', data,context_instance=RequestContext(request))
