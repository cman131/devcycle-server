from django import forms
from django.contrib.admin import widgets
from tour_config.models import TourConfig
from tour_config.fields import UnixDateTimeField
from django.utils.dateparse import parse_datetime
from django.utils.timezone import get_default_timezone
from datetime import datetime
from django.core.urlresolvers import reverse
from django.utils.translation import gettext as _
import logging

logger = logging.getLogger(__name__)

class TourConfigAddForm(forms.ModelForm):
    start_time = UnixDateTimeField(widget=widgets.AdminSplitDateTime)
    max_tour_time = UnixDateTimeField(label="End time", widget=widgets.AdminSplitDateTime)
    label_suffix = ":"
    class Meta:
        model = TourConfig
        exclude = ( 'is_cancelled' )

    def clean(self):
        cleaned_data = super(TourConfigAddForm, self).clean()
        start_time = cleaned_data.get('start_time')
        max_tour_time = cleaned_data.get('max_tour_time')

        if start_time and max_tour_time:
            if not start_time < max_tour_time:
                raise forms.ValidationError("Start Time must be before Max Tour Time")

        return cleaned_data


class TourConfigUpdateForm(TourConfigAddForm):
    class Meta:
        model = TourConfig
        exclude = ( 'is_cancelled', 'tour_id', 'gcm_sender_id', 'dcs_url' )


class ServerPollRateUpdateForm(forms.ModelForm):
    class Meta:
        model = TourConfig
        #exclude all but the server poll rate
        fields = ('server_polling_rate','server_polling_range',)
        labels = {
            'server_polling_rate' : _('Server Polling Rate'),
            'server_polling_range' : _('Server Polling Range'),
        }
        help_texts = {
            'server_polling_rate' : _('Server Polling Rate (sec)'),
            'server_polling_range' : _('Server Polling Range (sec)'),
        }




    def clean(self):
        cleaned_data = super(ServerPollRateUpdateForm, self).clean()

        server_polling_rate = cleaned_data.get('server_polling_rate')
        #The range for pushing to the server
        server_polling_range = cleaned_data.get('server_polling_range')

        #Ensure that polling range greater than 0
        if server_polling_range < 0:
          raise forms.ValidationError("Location Polling Rnage must be greater than 0 seconds")
        return cleaned_data

        # Ensure that the polling rate is 30 seconds or greater
        if server_polling_rate <= 30:
            raise forms.ValidationError("Server Polling Rate must be 30 seconds or greater")
        return cleaned_data

class LocationPollRateUpdateForm(forms.ModelForm):
    class Meta:
        model = TourConfig
        #exclude all but the location poll rate
        fields = ('location_polling_rate',)


    def clean(self):
        cleaned_data = super(LocationPollRateUpdateForm, self).clean()
        #The location polling rate, the device polling the location manager
        location_polling_rate = cleaned_data.get('location_polling_rate')

        # Ensure that the polling rate is 30 seconds or greater
        if location_polling_rate <= 5:
            raise forms.ValidationError("Location Polling Rate must be 5 seconds or greater")
        return cleaned_data
