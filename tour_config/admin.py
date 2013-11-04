from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.admin import ModelAdmin
from analysis.sites import tt_admin
from tour_config.models import TourRoute, TourConfig
from django.conf import settings

class TourRouteAdmin(OSMGeoAdmin):
    default_lat=4970088.468251135 #-74.005108 degrees
    default_lon=-8238210.93866121 #40.71291499 degrees
    default_zoom=13
    list_display = ('name',)
    openlayers_url = '/static/OpenLayers.js'
    change_form_template = 'tourroute_change_form.html'
    change_list_template = 'tourroute_list.html'
    delete_confirmation_template = 'tourroute_delete.html'
    delete_selected_confirmation_template = 'tourroute_delete.html'
    map_template = 'osm.html'
    wms_url = settings.MAP_TILE_SERVER

tt_admin.register(TourRoute, TourRouteAdmin)
