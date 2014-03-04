from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from tour_config.models import TourConfig
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView
from tour_config.forms import TourConfigAddForm, TourConfigUpdateForm, TourConfigPollRateUpdateForm
from django.core.urlresolvers import reverse_lazy, reverse
from urllib2 import urlopen, Request, URLError, HTTPError
from django.conf import settings
import json
from django.core import serializers
from django.core.cache import cache
from rider.models import Rider
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages
from tour_config.models import TourConfig
from tour_config.utils import set_polling_rate


import logging

logger = logging.getLogger(__name__)

class GetTourConfig(generics.RetrieveAPIView):
    model = TourConfig 
    slug_field = 'tour_id'
    slug_url_kwarg = 'tour_id'
    
    def get_serializer(self, instance=None, data=None,
                       files=None, partial=False):
        """
        Android expects UNIX timestamps in milliseconds and max_tour_time to be
        a time delta rather than a timestamp, so multiply them both by 1000
        and set max_tour_time to the difference between the two.
        Seriously, there's no reason this couldn't be done on the Android side
        instead.
        """
        if instance is not None:
            instance.start_time *= 1000
            instance.max_tour_time *= 1000
            instance.max_tour_time -= instance.start_time
        return super(GetTourConfig, self).get_serializer(instance=instance, data=data, files=files,
                                                         partial=partial)

class TourConfigUpdate(UpdateView):
    model = TourConfig
    form_class = TourConfigUpdateForm
    template_name = 'gcm.html'

    def get_success_url(self):
        """
        Return to same page on success. This view should be named
        'tour_config-update' in the urls of the admin site.
        """
        return reverse('gcm')

    def get_object(self, queryset=None):
        """
        Always grab the most recent TourConfig from the database, since for the
        initial release, we will only be working with a single tour at a time.
        """
        config = TourConfig.objects.latest('pk')
        return config if ( config is not None ) else None

    def form_valid(self, form):
        """
        Override form_valid functionality to send message via GCM to Android
        devices with new TourConfig
        """
        self.object = form.save(commit=False)
        push_ids = self.get_push_ids()
        headers = {}
        headers[settings.GCM_API_KEY_HEADER] = 'key='+settings.GCM_API_KEY
        headers['Content-Type'] = 'application/json'
        data = {}
        data['registration_ids'] = push_ids

        # Hack-y fix to get just the fields from the TourConfig instance
        newconfig = json.loads(serializers.serialize('json', [self.object]))[0]['fields']
        # Multiple the unix times stored in the database by 1000 because Android
        # uses milliseconds
        newconfig['start_time'] = newconfig['start_time']*1000
        newconfig['max_tour_time'] = newconfig['max_tour_time']*1000
        newconfig['max_tour_time'] = newconfig['max_tour_time'] - newconfig['start_time']
        data['data'] = {}
        data['data'][settings.JSON_KEYS['TOUR_CONFIG']] = newconfig
        # Comment out the following line to actually send messages
        #data['dry_run'] = True

        req = Request(settings.GCM_SEND_URL, json.dumps(data), headers)
        if len(push_ids) > 0:
            logger.debug('Sending request to GCM server:\n%s' % req.get_data())
            resp = urlopen(req)
            # TODO
            # Display a message on failure to send GCM message
        else:
            logger.debug('No push_ids registered; not sending updated config.')

        self.object = form.save()
        messages.success(self.request, 'Tour updated successfully.')

        set_polling_rate()

        return HttpResponseRedirect(self.get_success_url())

    def get_push_ids(self):
        return list(Rider.objects.values_list('push_id', flat=True).exclude(push_id__isnull=True).exclude(push_id__exact=''))

class TourConfigAdd(CreateView):
    model = TourConfig
    template_name = 'tourconfig_add_form.html'
    form_class = TourConfigAddForm

    def get_success_url(self):
        """
        Return to same page on success. This view should be named
        'tour_config-update' in the urls of the admin site.
        """
        return reverse('gcm')

    def form_valid(self, form):
        """
        Display a message upon successful tour creation.
        """
        response = super(TourConfigAdd, self).form_valid(form)
        messages.success(self.request, 'Tour created successfully.')

        set_polling_rate()

        return response

class TourConfigPollRateUpdate(UpdateView):
    model = TourConfig
    template_name = 'tourconfig_pollrate_update_form.html'
    form_class = TourConfigPollRateUpdateForm 

    def get_success_url(self):
        """
        Return to same page on success. This view should be named
        'tour_config-update' in the urls of the admin site.
        """
        return reverse('pollingrate/update/')

    def get_object(self, queryset=None):
        """
        Always grab the most recent TourConfig from the database, since for the
        initial release, we will only be working with a single tour at a time.
        """
        config = TourConfig.objects.latest('pk')
        return config if ( config is not None ) else None    

    def form_valid(self, form):
        """
        Display a message upon successful tour creation.
        """
        response = super(TourConfigPollRateUpdate, self).form_valid(form)
        messages.success(self.request, 'Poll Rate Updated Successfully.')

        set_polling_rate()

        return response