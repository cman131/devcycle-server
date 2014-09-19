# Change Notes:
# 09/18/2014 Team Centri-Pedal added this model to create Affinity Groups
# for TourTrak. These Affinity groups organize riders into groups that
# can be tracked on the map. It made sense to place it in the Rider Model
# beecause Many Riders make up and Affinity Group and many Affinity Groups
# can be assigned to a Rider.

from django.db import models
from django.core.validators import RegexValidator

class Rider(models.Model):
    id = models.AutoField(primary_key=True)
    os = models.CharField(max_length=125, null=True, blank=True)
    start_time = models.BigIntegerField(null=True, blank=True)
    push_id = models.CharField(max_length=512, null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True,editable=False)


class Affinity_Group(models.Model):
    id = models.AutoField(primary_key=True)
    #Regex is to ensure A-Z or a-z or digits. It also ensures a minumum length of at least 2 '{2,}'
    #Django does not have a min_length field.
    code = models.CharField(unique=True, max_length=4, validators=[RegexValidator(regex='^[a-zA-Z\d]{2,}$', message='Affinity Group Code can only be digits & letters and min length of 2')])
    description = models.CharField(max_length=255, null=True, blank=True) 
    registered_at = models.DateTimeField(auto_now_add=True,editable=False)
    riders = models.ManyToManyField(Rider, blank=True)