__author__ = 'ejm2095'
from rest_framework import serializers
from rider.models import Rider


class riderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rider

    def update(self, instance, attrs):
        # Update existing instance
        instance.push_id = attrs['push_id']
        instance.os = attrs['os']
        return instance

    def create(self, attrs):
        # Create new instance
        return Rider(**attrs)
