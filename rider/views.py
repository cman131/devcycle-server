import logging
import json
from rider.models import Rider, Affinity_Group_Mapping
from affinity.models import Group
from rider.serializer import riderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rider.rider_id_tools import create_uuid, decrypt_uuid
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse

logger = logging.getLogger(__name__)

def list_group_view(request, r_id):
	json_data = []
	aff_data = Affinity_Group_Mapping.objects.filter(rider=r_id)
	for r in aff_data:
	    aff_id = r['affinity_group']
		group_data = Group.objects.get(id=aff_id)
		json_data.add({'name':group_data.name,'id':aff_id})
	return JsonResponse(json.dumps(json_data))
def create_group_view(request, name, aff_id, r_id):
    group = Group(name=name,code=aff_id)
	agm = Affinity_Group_Mapping(rider=r_id,affinity_group=aff_id)
	group.save()
	agm.save()
	return HttpResponse(status=status.HTTP_201_CREATED)
def join_group_view(request, aff_id, r_id):
	agm = Affinity_Group_Mapping(rider=r_id,affinity_group=aff_id)
	agm.save()
	return HttpResponse(status=status.HTTP_201_CREATED)
def leave_group_view(request, aff_id, r_id):
	agm = Affinity_Group_Mapping.get(rider=r_id).filter(affinity_group=aff_id)
	agm.delete()
	return HttpResponse(status=status.HTTP_201_CREATED)
	
class RiderAPI(APIView):

    def post(self, request, format=None):
        try:
            logger.debug('trying')
            data = request.DATA
            serializer = riderSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                rider_uuid = create_uuid(serializer.object.pk)

                return Response(
                    {settings.JSON_KEYS['RIDER_ID']: rider_uuid},
                    status=status.HTTP_201_CREATED
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as ex:
            return Response(
                {settings.JSON_KEYS['BAD_REQ']: ex.message},
                status=status.HTTP_400_BAD_REQUEST
            )


class RiderPushUpdateAPI(APIView):

    def post(self, request, format=None):
        data = request.DATA
        id = decrypt_uuid(data[settings.JSON_KEYS['RIDER_ID']])
        try:
            rider = Rider.objects.get(id=id)
            rider.push_id = data.get(settings.JSON_KEYS['RIDER_PUSH_ID'], '')
            rider.save()

            return Response(
                {settings.JSON_KEYS['RIDER_ID']:
                    data[settings.JSON_KEYS['RIDER_ID']]},
                status=status.HTTP_201_CREATED
            )

        except Exception as ex:
            return Response(
                {settings.JSON_KEYS['BAD_REQ']: ex.message},
                status=status.HTTP_400_BAD_REQUEST
            )
