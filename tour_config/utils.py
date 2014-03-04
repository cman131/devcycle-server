from django.core.cache import cache
from tour_config.models import TourConfig


def set_polling_rate():
    """ Cache the Polling Rate """
    #Set Polling Rate in Cache on Creation
    tour = TourConfig.objects.latest('pk') # Get the latest tour
    cache.set(settings.JSON_KEYS['POLLING_RATE'], tour.polling_rate)
    return
