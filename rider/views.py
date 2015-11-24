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
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotAllowed, Http404


logger = logging.getLogger(__name__)


def list_group_view(request, r_id):
    # Check that the rider exists
    rider_exists = Rider.objects.filter(id=r_id).exists()
    if not rider_exists:
        write_response(request, json.dumps([{"success":"false","message":"ERROR: Rider does not exist"}]))

    # response object placeholder
    json_data = []
    json_data.append({"success": "true", "message": "success"}) #can assume success since if we fail this never gets returned

    # get the list of groups the rider is associated with
    rider_groups = Group.objects.filter(rider__id=r_id)
    # check that they're in a group
    if rider_groups:
        # iterate over groups they're in
        # get the group ID and group name to return to the client
        for group in rider_groups:
            # affinity_group = group.code
            affinity_group = group.id
            group_data = Group.objects.get(id=affinity_group)
            # json_data.append({'name':group_data.name,'id':affinity_group})
            json_data.append({'name':group_data.name,'code':group_data.code})
    # return the group data as a JSON response and set the response type appropriately
    # return HttpResponse('callback('+json.dumps(json_data)+');', content_type="application/json")
    return write_response(request, json.dumps(json_data))


@csrf_exempt
def create_group_view(request):
    # make sure the request is a POST request and that form data has been provided
    if request.method == "POST" and request.POST:
        # Extract the necessary info from the request
        post_data = request.POST
        group_name = post_data['name']
        rider_id = post_data['rider_id']
        aff_code = post_data['aff_code']

        # Check if group code is already in use
        # if group test doesn't come back empty, return a bad request error
        group_test = Group.objects.filter(code=aff_code)
        if group_test:
            return write_response(request, json.dumps([{"success":"false", "message":"ERROR: Group code in use"}]))

        # Create a new group with the requested name and affinity code
        group = Group(name=group_name, code=aff_code)
        group.save()

        # Get the PK of the new group and create a mapping to a rider
        group_id = Group.objects.get(code=aff_code).id
        agm = Affinity_Group_Mapping(rider_id=rider_id, affinity_group_id=group_id)
        agm.save()

        # return a success code
        return write_response(request, json.dumps([{"success":"true", "message":"Sucess"}]))
    # return an error - tells client that only POST is allowed
    # response = HttpResponseNotAllowed(['POST'])
    # response.write("ERROR: Only POST requests allowed")
    # return response

    # returning a 404 so that the link looks invalid from the outside
    raise Http404


def join_group_view(request, aff_id, r_id):
    # Check if the group exists
    group_exists_test = Group.objects.filter(code=aff_id)
    if not group_exists_test:
        return write_response(request, json.dumps([{"success": "false", "message": "ERROR: Group does not exist"}]))

    # Check if the rider is already in the group
    rider_in_group_test = Group.objects.filter(rider__id=r_id).filter(code=aff_id)
    # if group_test isn't empty, return an error code
    if rider_in_group_test:
        return write_response(request, json.dumps([{"success": "false", "message": "ERROR: already in group"}]))

    # Get the numerical ID that matches the group's affinity code
    # Then create a mapping from the rider to the group
    group_id=Group.objects.get(code=aff_id).id
    agm = Affinity_Group_Mapping(rider_id=r_id,affinity_group_id=group_id)
    agm.save()

    # return a success response
    group_name = [{'success': 'true', 'message': 'success'}, {'name' : group_exists_test[0].name}]
    return write_response(request, json.dumps(group_name))


def leave_group_view(request, aff_id, r_id):
    # Check that the group exists
    group_exists_test = Group.objects.filter(code=aff_id)
    if not group_exists_test:
        return write_response(request, json.dumps([{"success": "false", "message": "ERROR: Group does not exist"}]))

    # Check that the rider is in the group
    rider_in_group_test = Group.objects.filter(rider__id=r_id).filter(code=aff_id)
    if not rider_in_group_test:
        return write_response(request, json.dumps([{"success": "false", "message": "ERROR: Not in group"}]))

    # Get the numerical ID that matches the group's affinity code
    # Then find the mapping entry in the Affinity Group Mapping table and delete it
    group_id=Group.objects.get(code=aff_id).id
    agm = Affinity_Group_Mapping.objects.filter(rider_id=r_id).filter(affinity_group_id=group_id)
    agm.delete()

    # return a success response - need to include the callback key for JSONP requests
    return write_response(request, json.dumps([{"success": "true", "message": "Success"}]))


def check_code_view(request, aff_id):	
    # check if the code is in use
    # if group_test doesn't come back empty return a 400 error code
    group_test = Group.objects.filter(code=aff_id)
    if group_test:
        return write_response(request, json.dumps([{"success": "false", "message": "Code exists"}]))
    return write_response(request, json.dumps([{"success": "true", "message": "Code does not exist"}]))


def write_response(request, data):
    response = HttpResponse()
    response.content_type="application/json"

    if 'callback' in request.REQUEST:
        return_string = '%s(%s)' % (request.REQUEST['callback'], data)
        response.write(return_string)
        return response
    response.write(data)
    return response


class RiderAPI(APIView):

    def post(self, request, format=None):
        try:
            data = request.data
            logger.debug('[RiderAPI:Register] Attempting to find rider with id: '+str(data[u'id']))
            rider_exists = Rider.objects.filter(id=data[u'id']).exists()
            if rider_exists:
                logger.debug('[API:Register] Rider' + str(data[u'id']) + 'was already registered.')
            else:
                logger.debug('[RiderAPI:Register] Rider with id: ' + str(data[u'id'] + ' was not found. Registering...'))
                serializer = riderSerializer(data=data)
                if not serializer.is_valid():
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )
                rider_data = serializer.save()
                rider_data.save()
                logger.debug('[RiderAPI:Register] Rider' + str(rider_data.id) + 'has been registered.')

            return Response(
                {settings.JSON_KEYS['RIDER_ID']: data[u'id']},
                status=status.HTTP_201_CREATED
            )

        except Exception as ex:
            return Response(
                {settings.JSON_KEYS['BAD_REQ']: ex.message},
                status=status.HTTP_400_BAD_REQUEST
            )


class RiderPushUpdateAPI(APIView):

    def post(self, request, format=None):
        data = request.data
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
