__author__ = 'ejm2095'
from rest_framework import serializers
from location_update.models import Location


class locationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance.
        """
        if instance:
            # Update existing instance
            instance.coords = attrs['coords']
            instance.speed = attrs['speed']
            instance.time = attrs['time']
            instance.accuracy = attrs['accuracy']
            instance.rider = attrs['rider']

            return instance

        # Create new instance
        return Location(**attrs)
