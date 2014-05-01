import logging
import traceback
from location_update.models import Location
from location_update.serializers import locationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render_to_response
from django.template import RequestContext
from rider.models import Rider
from rider.rider_id_tools import decrypt_uuid
from rider.utils import get_registration_data, get_num_registered
from django.conf import settings
from django.contrib.gis.geos import Point
from rider.models import Rider
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.db import connection
from tour_config.models import TourConfig
import time
import math
from django.core import serializers


logger = logging.getLogger(__name__)


class LocationAPI(APIView):

    def post(self, request, format=None):
        try:

            ###
            # This won't work without the header
            # 'Content-Type: application/json' :
            data = request.DATA
            ###

            # Get the Locations from Data
            loc_data = data.get(settings.JSON_KEYS['LOCATIONS'])

            # Get the Tour_Id name from Data
            tour_id = data.get('tour_id')

            # Get and decrypt the UUID
            rider = decrypt_uuid(data[settings.JSON_KEYS['RIDER_ID']])

	    logger.error("RIDER TO PRINT HERE: ", rider)

            # Check if the parameters passed in 
            # exist in the database before saving
            # Get Current Tour
            curr_tour = TourConfig.objects.get(tour_id=tour_id)

            if curr_tour is None: 
                raise Exception("Tour '%s' Does Not Exist" % (data.get('tour_id')) )

            if rider is None:
                raise Exception("Rider Id Does Not Exist")

            # Go through the points and store it into the database
            loc_list = []
            for point in loc_data:
                time = long(point.get(settings.JSON_KEYS['LOC']['TIME']))

                location = Location(
                        rider=Rider(pk=rider),
                        tour_id=TourConfig(tour_id=tour_id),
                        coords=Point(
                                  point.get(settings.JSON_KEYS['LOC']['LON']),
                                  point.get(settings.JSON_KEYS['LOC']['LAT'])
                                  ),
                        accuracy=point.get(
                                  settings.JSON_KEYS['LOC']['ACC']),
                        speed=point.get(
                                  settings.JSON_KEYS['LOC']['SPEED']),
                        bearing=point.get(
                                  settings.JSON_KEYS['LOC']['BEARING']),
                        battery=point.get(
                                  settings.JSON_KEYS['LOC']['BATT_LVL']),
                        provider=point.get(
                                  settings.JSON_KEYS['LOC']['PROVIDER']),
                        time=(time/1000)
                    )

                loc_list.append(location)

            # if there was not any errors send back a 201
            # other wise send 400 and a response
            # This is where the locations are 
            # being saved the database
            Location.objects.bulk_create(loc_list)

            # Get server polling rate from db
            server_polling_rate = curr_tour.server_polling_rate

            # Get server polling range from db
            server_polling_range = curr_tour.server_polling_range

            # Get location polling rate from db
            location_polling_rate = curr_tour.location_polling_rate


            return Response(
                {
                settings.JSON_KEYS['SERVER_POLLING_RATE']: server_polling_rate,
                settings.JSON_KEYS['SERVER_POLLING_RANGE']: server_polling_range,
                settings.JSON_KEYS['LOCATION_POLLING_RATE']: location_polling_rate
                },
                status=status.HTTP_201_CREATED
                )

        except Exception as ex:
            logger.info(traceback.format_exc())

            return Response(
                {settings.JSON_KEYS['BAD_REQ']: ex.args},
                status=status.HTTP_400_BAD_REQUEST
            )
        # end except
    #end post()

    def get(self, request, format=None):
        df = DateFormat(datetime.now())
        mins_ago = long(df.U()) - 500 #10 mins
        riders = {}

        cursor = connection.cursor()
        cursor.execute(
            """SELECT rider_id, speed, ST_X(coords), ST_Y(coords)
                FROM (
                    SELECT rider_id, speed, coords,
                    RANK() OVER (PARTITION BY rider_id ORDER BY time DESC) as rank
                        FROM location_update_location
                    WHERE speed != 0)dt
                WHERE dt.rank <= 10""")

        for row in cursor.fetchall():
            (rider_id, speed, lon, lat)=row
            if not riders.has_key(rider_id):
                riders[rider_id] = []
            riders[rider_id].append((int(speed), lon, lat))
        riders = riders.values()
        return Response(
                    {'locations': riders}, status=status.HTTP_200_OK)

'''
Used for displaying the last known position of every rider in the DB
'''
class RecentLocationAPI(APIView):

    def post(self, request, format=None):
        return Response(
                {settings.JSON_KEYS['BAD_REQ']: ex.args},
                status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        #Latest tour used for the total number of riders
        tour = TourConfig.objects.latest('pk') # Get the latest tour

        df = DateFormat(datetime.now())
        end_interval = tour.start_time#long(df.U())
        poll_rate = tour.server_polling_rate
        poll_range = tour.server_polling_range

        #Sever's poling range+polling interval ago.
        start_interval = end_interval - poll_rate -poll_range

        rider_count = Rider.objects.count()
        riders = {}

        cursor = connection.cursor()
        cursor.execute(
            """SELECT rider_id, speed, ST_X(coords), ST_Y(coords)
                   FROM location_update_location
                WHERE time BETWEEN %s AND %s LIMIT %s""",
                [start_interval, end_interval, rider_count])
        for row in cursor.fetchall():
            (rider_id, speed, lon, lat)=row
            if not riders.has_key(rider_id):
                riders[rider_id] = []
            riders[rider_id].append((int(speed), lon, lat))
        riders = riders.values()
        return Response(
                {'locations': riders}, status=status.HTTP_200_OK)
'''
                {'mins_ago': start_interval,
                'time': end_interval,
                'poll_rate': poll_rate,
                'poll_range': poll_range,
                'rider_count': rider_count }, status=status.HTTP_200_OK)
'''


class RouteAPI(APIView):
    def get(self, request, format=None):
        config = TourConfig.objects.latest('pk')

        if config.tour_route is not None:
            return Response( {'route': config.tour_route.route},
                             status=status.HTTP_200_OK )
        else:
            return Response( {'route': []},
                             status=status.HTTP_200_OK )

class PlaybackAPI(APIView):
    def get(self, request, format=None):
        playback_interval = 300
        block_size = 3

        block = int(request.GET['block'])
        frames = []
        cursor = connection.cursor()
        config = TourConfig.objects.latest('pk')

        start_time = config.start_time
        end_time = config.max_tour_time
        max_time = min(time.time(), end_time)

        if max_time <= start_time:
            return Response({'frames': [], 'total': 0}, status=status.HTTP_200_OK)

        total_time = max_time - start_time;
        total = int(math.ceil(total_time / playback_interval)) # 10 mins

        for cur_interval in range(block, block+block_size):
            if not block < total:
                break

            start_interval = start_time + (playback_interval * cur_interval)
            end_interval = start_interval + playback_interval

            cursor.execute(
                """SELECT rider_id, speed, ST_X(coords), ST_Y(coords)
                       FROM location_update_location
                    WHERE speed != 0 AND time BETWEEN %s AND %s
                """, [start_interval, end_interval])

            frame = []
            frame.append({'start': start_interval,
                                         'end': end_interval});
            for row in cursor.fetchall():
                (rider_id, speed, lat, lon)=row
                frame.append((int(speed), lat, lon))
            frames.append(frame);
        return Response(
                    {'frames': frames, 'total': total}, status=status.HTTP_200_OK)
