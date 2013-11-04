from django.conf import settings
from datetime import datetime
from django.utils.dateformat import DateFormat
from location_update.models import Location
from django.core.cache import cache
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db import connection

__author__ = 'ejm2095'

from celery import task


@task()
def update_num_riders():
    df = DateFormat(datetime.now())
    # Search within past 15 minutes
    tm = long(df.U()) - 900
    number_riders = Location.objects.filter(
        time__gte=tm).distinct('rider').count()

    cache.set(settings.JSON_KEYS['RIDER_CNT'], number_riders)
    return number_riders

@task
def build_all_speed():
    cursor = connection.cursor()
    cursor.execute(
            """UPDATE location_update_location la
                    SET speed =
                        COALESCE((
                            SELECT
                                ST_Distance_Spheroid(la.coords,lb.coords,'SPHEROID["WGS 84",6378137,298.257223563]')/(la.time - lb.time)
                            FROM location_update_location lb
                            WHERE lb.rider_id = la.rider_id
                                AND lb.time < la.time
                            ORDER BY lb.time DESC
                            LIMIT 1), 0)
                        WHERE la.speed IS NULL;
                        """)
    return cursor.rowcount
