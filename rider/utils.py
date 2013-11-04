import random
from django.db.models import Count
import pytz
from django.core.cache import cache
from rider.models import Rider
from datetime import datetime, timedelta, date
#
#
def build_registration_data():
    rider_counts = []
    col = {}
    now = datetime.now(tz=pytz.utc)
    data = Rider.objects.extra(select={'dayMonth': "to_char(registered_at, 'MMDD')"}).values('dayMonth').annotate(dcount=Count('registered_at'))
    for r in data:
        d = r['dayMonth']
        day = datetime(now.year, int(d[0:2]), int(d[2:4]))
        col[day.strftime("%Y-%m-%d")] = r['dcount']
    times = col.keys()
    times.sort()
    for r in times:
        rider_counts.append(col[r])
    return {"graph_label":times,"graph_values":rider_counts, "reg_compiled":now}

def test():
    return Rider.objects.extra(select={'dayMonth': "to_char(registered_at, 'MMDD')"}).values('dayMonth').annotate(dcount=Count('registered_at'))

def get_registration_data():
    reg_data = cache.get('registrations')
    if reg_data and reg_data.get("reg_compiled") > (datetime.now(tz=pytz.utc)+timedelta(hours=3)):
        return reg_data
    reg_data = build_registration_data()
    cache.set('registrations', reg_data)

    return reg_data

def get_num_registered():
    riders = cache.get('num_registration')
    now = datetime.now(tz=pytz.utc)
    if riders and riders.get('compiled') > (now+timedelta(hours=1)):
        return riders
    riders = Rider.objects.count()
    data = {'num_riders':riders,"compiled":now}
    cache.set('num_registration', data)
    return  data
#
def build_os_data():
    os_data = []
    os = Rider.objects.values('os').annotate(os_count=Count('os'))

    for i in os:
        data = {'os': i['os'], 'count': i['os_count'], 'color': gen_colors()}
        os_data.append(data)
    now = datetime.now(tz=pytz.utc)
    return {"os_data":os_data, "os_compiled":now}
#
#
def get_os_data():
    reg_data = cache.get('os_info')
    if reg_data and reg_data.get("os_compiled") > (datetime.now(tz=pytz.utc)+timedelta(hours=3)):
        return reg_data
    reg_data = build_os_data()
    cache.set('os_info', reg_data)
    return reg_data
#
def gen_colors():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())
