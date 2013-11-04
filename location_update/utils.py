__author__ = 'ejm2095'

import random
import pytz
import time
from django.db.models import Avg, Max, Min, Count
from django.core.cache import cache
from datetime import datetime, timedelta
from location_update.models import Location



def build_update_data():
    loc_counts = []
    now = datetime.now(tz=pytz.utc)
    col = {}
    data = Location.objects.extra(select={'up_time': "time/1000"}).values('up_time').annotate(dcount=Count('coords'))
    for r in data:
        d = r['up_time']*1000
        ts = datetime.fromtimestamp(d).strftime('%Y-%m-%d %H:%M:%S')
        col[ts] = r['dcount']
    times = col.keys()
    times.sort()
    for r in times:
        loc_counts.append(col[r])
    return {"graph_values":loc_counts,'graph_label':times, "dist_up_compiled":now}

def get_update_data():
    loc_data = cache.get('dist_updates')
    if loc_data and loc_data.get("dist_up_compiled") > (datetime.now(tz=pytz.utc)+timedelta(minutes=15)):
        return loc_data
    loc_data = build_update_data()
    cache.set('dist_updates', loc_data)
    return loc_data

def build_battery_info():
    avg_battery = []
    times = []
    col = {}
    now = datetime.now(tz=pytz.utc)
    data = Location.objects.extra(select={'up_time': "time/1000"}).values('up_time').annotate(davg=Avg('battery'))
    for r in data:
        d = r['up_time']*1000
        ts = datetime.fromtimestamp(d).strftime('%Y-%m-%d %H:%M:%S')
        col[ts] = r['davg']
    times = col.keys()
    times.sort()
    for r in times:
        avg_battery.append(col[r])
    return {"graph_values":avg_battery,
            'graph_label':times,
            "bat_compiled":now}

def get_battery_info():
    bat_info = cache.get('battery_info')
    if bat_info and bat_info.get("bat_compiled") > (datetime.now(tz=pytz.utc)+timedelta(minutes=15)):
        return bat_info
    bat_info = build_battery_info()
    cache.set('battery_info', bat_info)
    return bat_info

def get_location_updates():
    locs = cache.get('number_updates')
    now = datetime.now(tz=pytz.utc)
    if locs and locs.get("compiled") > (now+timedelta()):
            return locs
    num = Location.objects.count()
    locs = {"num_locations": num,"compiled":now}
    cache.set('number_updates', locs)
    return locs
