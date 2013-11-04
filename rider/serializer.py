__author__ = 'ejm2095'
from rest_framework import serializers
from rider.models import Rider


class riderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rider

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance.
        """
        if instance:
            # Update existing instance
            instance.push_id = attrs['push_id']
            instance.os = attrs['os']
            return instance

        # Create new instance
        return Rider(**attrs)
