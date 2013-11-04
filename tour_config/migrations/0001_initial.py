# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TourConfig'
        db.create_table('tour_config_tourconfig', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tour_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('tour_logo', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('tour_id', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('tour_organization', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('dcs_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('gcm_sender_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('max_tour_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('tour_route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tour_config.TourRoute'])),
        ))
        db.send_create_signal('tour_config', ['TourConfig'])

        # Adding model 'TourRoute'
        db.create_table('tour_config_tourroute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('route', self.gf('django.contrib.gis.db.models.fields.MultiLineStringField')()),
        ))
        db.send_create_signal('tour_config', ['TourRoute'])


    def backwards(self, orm):
        # Deleting model 'TourConfig'
        db.delete_table('tour_config_tourconfig')

        # Deleting model 'TourRoute'
        db.delete_table('tour_config_tourroute')


    models = {
        'tour_config.tourconfig': {
            'Meta': {'object_name': 'TourConfig'},
            'dcs_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'gcm_sender_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_tour_time': ('django.db.models.fields.DateTimeField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'tour_id': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
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