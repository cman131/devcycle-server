{% extends 'gis/admin/openlayers.js' %}
{% block base_layer %} new OpenLayers.Layer.OSM("OSM Layer", "{{ wms_url }}/osm/${z}/${x}/${y}.png", {numZoomLevels: 18}); {% endblock %}
