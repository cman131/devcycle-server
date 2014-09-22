# Change Notes:
# 09/18/2014 Team Centri-Pedal edited this model to contain a many to 
# many relationship with an Affinity Group

from django.db import models
from django.core.validators import RegexValidator

class Affinity_Group(models.Model):
    id = models.AutoField(primary_key=True)
    #Regex is to ensure A-Z or a-z or digits. It also ensures a minumum length of at least 2 '{2,}'
    #Django does not have a min_length field.
    code = models.CharField(unique=True, max_length=4, validators=[RegexValidator(regex='^[a-zA-Z\d]{2,}$', message='Affinity Group Code can only be digits & letters and min length of 2')])
    description = models.CharField(max_length=255, null=True, blank=True) 
    registered_at = models.DateTimeField(auto_now_add=True,editable=False)

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