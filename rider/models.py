from django.db import models


class Rider(models.Model):
    id = models.AutoField(primary_key=True)
    os = models.CharField(max_length=125, null=True, blank=True)
    start_time = models.BigIntegerField(null=True, blank=True)
    push_id = models.CharField(max_length=512, null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True,editable=False)
