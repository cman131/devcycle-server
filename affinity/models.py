# Change Notes:
# 09/18/2014 Team Centri-Pedal added this model to create the notion
# of Affinity Groups that riders can join.

from django.db import models
from django.core.validators import RegexValidator

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    #Regex is to ensure A-Z or a-z or digits. It also ensures a minumum length of at least 3 '{3,}'
    #Django does not have a min_length field.
    code = models.CharField(unique=True, max_length=7, validators=[RegexValidator(regex='^[a-zA-Z\d]{3,}$', message='Affinity Group Code can only be digits & letters and min length of 3')])
    description = models.CharField(max_length=255, null=True, blank=True) 
    registered_at = models.DateTimeField(auto_now_add=True,editable=False)