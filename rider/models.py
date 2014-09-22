# Change Notes:
# 09/18/2014 Team Centri-Pedal edited this model to contain a many to 
# many relationship with an Affinity Group

from django.db import models
from django.core.validators import RegexValidator

class Rider(models.Model):
    id = models.AutoField(primary_key=True)
    os = models.CharField(max_length=125, null=True, blank=True)
    start_time = models.BigIntegerField(null=True, blank=True)
    push_id = models.CharField(max_length=512, null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True,editable=False)
    affinity_group = models.ManyToManyField(AffinityGroup, through='RiderAffinityGroupRelationship')

class RiderAffinityGroupRelationship(models.Model):
	rider = models.ForeignKey(Rider)
	affinitygroup = models.ForeignKey(AffinityGroup)