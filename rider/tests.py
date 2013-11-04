import json

from django.test import LiveServerTestCase
from django.test.client import Client
from django.conf import settings
from rider.rider_id_tools import create_uuid, decrypt_uuid


class RiderTest(LiveServerTestCase):
    def setUp(self):
        self.c = Client()

    def test_uuid(self):
        varLittle = 1
        varBig = 5678912
        varLittle_res = 'TcH4FR09ROSA4b42WJX6i/NzzjzbX3p7U62YCZUE4CE=\n'
        varBig_res = 'TcH4FR09ROSA4b42WJX6i7vdGEPO+K9i9fJybUAKFA0=\n'
#        assert that the start data is correct
        self.assertEquals(varLittle, decrypt_uuid(varLittle_res))
        self.assertEquals(varBig, decrypt_uuid(varBig_res))
#        test creating UUID
        testLittle = create_uuid(varLittle)
        testBig = create_uuid(varBig)
        self.assertEquals(testLittle, varLittle_res)
        self.assertEquals(testBig, varBig_res)
#        test decryption
        testLittle = decrypt_uuid(testLittle)
        testBig = decrypt_uuid(testBig)
        self.assertEquals(testLittle, varLittle)
        self.assertEquals(testBig, varBig)

    def test_rider_api(self):
#        data
        headers = [('Content-Type', 'application/json')]
        request_data = {'os': 'testOS', 'push_id': 'abc123'}
#        perform post request
        r = self.c.post('/register/', data=request_data, headers=headers)
#        assert results
        self.assertEqual(r.status_code, 201)
        data = json.loads(r.content)
        self.assertIsNotNone(data.get(settings.JSON_KEYS['RIDER_ID']))
