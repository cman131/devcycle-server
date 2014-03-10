from django.core.cache import cache
from tour_config.models import TourConfig
from django.conf import settings

def set_server_polling_rate():
    """ Cache the Polling Rate """
    #Set Server Polling Rate in Cache on Creation
    tour = TourConfig.objects.latest('pk') # Get the latest tour
    cache.set(settings.JSON_KEYS['SERVER_POLLING_RATE'], tour.server_polling_rate)
    return
