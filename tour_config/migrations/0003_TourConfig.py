# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'TourConfig.tour_id'
        db.alter_column('tour_config_tourconfig', 'tour_id', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64))
        # Adding unique constraint on 'TourConfig', fields ['tour_id']
        db.create_unique('tour_config_tourconfig', ['tour_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'TourConfig', fields ['tour_id']
        db.delete_unique('tour_config_tourconfig', ['tour_id'])


        # Changing field 'TourConfig.tour_id'
        db.alter_column('tour_config_tourconfig', 'tour_id', self.gf('django.db.models.fields.SlugField')(max_length=256))

    models = {
        'tour_config.tourconfig': {
            'Meta': {'object_name': 'TourConfig'},
            'dcs_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'gcm_sender_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_tour_time': ('django.db.models.fields.DateTimeField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
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