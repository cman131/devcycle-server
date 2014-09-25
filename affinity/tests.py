from django.test import TestCase
from affinity.models import Group
from rider.models import Rider
from rider.models import Affinity_Group_Mapping
import datetime

#Test the affinity group rider relation
class Test_AGR_Relation(TestCase):

    def setUp(self):
        now = datetime.datetime.now()
        Rider.objects.create('android', '2932939293923932', '4434344', now)
        Rider.objects.create('iOS', '5434932452', '882937823828', now)
        Rider.objects.create('kindle', '832992323923923', '949394344', now)
        Group.objects.create('RMCD', 'House of Ronald McDonald', now)
        Group.objects.create('BIKENY', 'The BIKE NY riders', now)
        Group.objects.create('ZONE', 'Zonies', now)

        ##Aff group Rider
        Affinity_Group_Mapping.objects.create(1, 2)
        Affinity_Group_Mapping.objects.create(1, 2)
        Affinity_Group_Mapping.objects.create(1, 2)

        #self.assertEqual(1 + 1, 2)
