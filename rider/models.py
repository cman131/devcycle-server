# Change Notes:
# 09/18/2014 Team Centri-Pedal edited this model to contain a many to 
# many relationship between a rider and a newly added Affinity Group 
# that users of TourTrak will be able to join. This many to many relationship 
#will be mapped to the Rider_Affinity_Group_Mapping table in SQL

from django.db import models
from django.core.validators import RegexValidator
from affinity.models import Group

class Rider(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    os = models.CharField(max_length=125, null=True, blank=True)
    start_time = models.BigIntegerField(null=True, blank=True)
    push_id = models.CharField(max_length=512, null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True,editable=False)
    affinity_group = models.ManyToManyField(Group, through='Affinity_Group_Mapping')

class Affinity_Group_Mapping(models.Model):
    rider = models.ForeignKey(Rider)
    affinity_group = models.ForeignKey(Group)

#Ensure uniquness of the rider and affinity_group together so no duplicates.
    class Meta:
        unique_together = ('rider', 'affinity_group')
