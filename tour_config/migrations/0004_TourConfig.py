# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'TourConfig.start_time'
        db.delete_column('tour_config_tourconfig', 'start_time')

        # Deleting field 'TourConfig.max_tour_time'
        db.delete_column('tour_config_tourconfig', 'max_tour_time')

        # Adding field 'TourConfig.start_time_new'
        db.add_column('tour_config_tourconfig', 'start_time_new',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'TourConfig.max_tour_time_new'
        db.add_column('tour_config_tourconfig', 'max_tour_time_new',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'TourConfig.start_time'
        db.add_column('tour_config_tourconfig', 'start_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 4, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'TourConfig.max_tour_time'
        db.add_column('tour_config_tourconfig', 'max_tour_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 4, 3, 0, 0)),
                      keep_default=False)

        # Deleting field 'TourConfig.start_time_new'
        db.delete_column('tour_config_tourconfig', 'start_time_new')

        # Deleting field 'TourConfig.max_tour_time_new'
        db.delete_column('tour_config_tourconfig', 'max_tour_time_new')


    models = {
        'tour_config.tourconfig': {
            'Meta': {'object_name': 'TourConfig'},
            'dcs_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'gcm_sender_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_tour_time_new': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'start_time_new': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tour_id': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'}),
            'tour_logo': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'tour_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'tour_organization': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'tour_route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tour_config.TourRoute']"})
        },
        'tour_config.tourroute': {
            'Meta': {'object_name': 'TourRoute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'route': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {})
        }
    }

    complete_apps = ['tour_config']