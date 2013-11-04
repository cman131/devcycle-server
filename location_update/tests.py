import json
import urllib2
import urlparse
from django.test import LiveServerTestCase
from django.test.utils import override_settings
from rider.rider_id_tools import create_uuid
from django.conf import settings
from rest_framework import status

"""
This test case uses a live server because using the dummy django client
doesn't work. Something to do with the REST Framework, methinks.
Instead, this uses urllib2 to make the request.
@author jmd2188
"""

TEST_CACHE = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


class LocationUpdateTest(LiveServerTestCase):
    fixtures = ['seven_riders.json']
    headers = {'Content-Type': 'application/json'}

    def setUp(self):
        self.my_id = create_uuid(1).encode('unicode_escape')
        self.location_update_url = urlparse.urljoin(
            self.live_server_url, '/location_update/'
        )
    #end setUp

    def test_sendLocationUpdate(self):
        data = load_update_req('idealRequest.json')
        self.sendRequest(data)
    #end test_sendLocationUpdate

    def test_badRiderId(self):
        data = load_update_req('badRiderIdRequest.json')
        self.sendBadRequest(data)
    #end test_badRiderId

    def test_onlyRequiredFields(self):
        data = load_update_req('onlyRequiredFieldsRequest.json')
        self.sendRequest(data)
    #end test_onlyRequiredFields

    def test_missingRequiredFields(self):
        data = load_update_req('missingRequiredFieldsRequest.json')
        self.sendBadRequest(data)

    def sendRequest(self, data):
        req = urllib2.Request(
            url=self.location_update_url, data=data, headers=self.headers
        )
        resp = urllib2.urlopen(req)

        self.assertEqual(resp.getcode(), status.HTTP_201_CREATED)

        respData = resp.read()
        try:
            obj = json.loads(respData)
        except Exception as e:
            self.fail('Could not decode response body as JSON: ' + e.message)

        self.assertIsNotNone(obj[settings.JSON_KEYS['RIDER_CNT']])
        ## not sure we can test this with memcached
        #self.assertEqual(
        #    obj[settings.JSON_KEYS['RIDER_CNT']],
        #    Rider.objects.count())
        ##
    #end sendRequest

    def sendBadRequest(self, data):
        req = urllib2.Request(
            url=self.location_update_url, data=data, headers=self.headers
        )
        with self.assertRaises(urllib2.HTTPError) as cm:
            urllib2.urlopen(req)
        ex = cm.exception
        self.assertEqual(ex.code, status.HTTP_400_BAD_REQUEST)
    #end sendBadRequest


def load_update_req(fn):
    json_s = ""
    with open('location_update/fixtures/' + fn) as f:
        for line in f:
            json_s += line

    return json_s
