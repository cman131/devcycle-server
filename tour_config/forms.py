from django import forms
from django.contrib.admin import widgets
from tour_config.models import TourConfig
from tour_config.fields import UnixDateTimeField
from django.utils.dateparse import parse_datetime
from django.utils.timezone import get_default_timezone
from datetime import datetime
from django.core.urlresolvers import reverse
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


class TourConfigPollRateUpdateForm(forms.ModelForm):
    class Meta:
        model = TourConfig
        #exclude all but the poll rate
        fields = ('polling_rate',)


    def clean(self):
        cleaned_data = super(TourConfigPollRateUpdateForm, self).clean()
        polling_rate = cleaned_data.get('polling_rate')

        # Ensure that the polling rate is 30 seconds or greater
        if polling_rate <= 30:
            raise forms.ValidationError("Polling Rate must be 30 seconds or greater")
        return cleaned_data
