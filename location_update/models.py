from django.contrib.gis.db import models
from rider.models import Rider

class Location(models.Model):
    coords = models.PointField()
    speed = models.FloatField(null=True, blank=True, default=None)
    time = models.BigIntegerField()
    accuracy = models.FloatField(null=True, blank=True, default=None)
    rider = models.ForeignKey(Rider)
    battery = models.FloatField(null=True, blank=True, default=None)
    provider = models.CharField(max_length=50, blank=True, default=None)
    bearing = models.FloatField(null=True, blank=True, default=None)
    tour_id = models.ForeignKey('tour_config.TourConfig', to_field='tour_id', on_delete=models.PROTECT)
