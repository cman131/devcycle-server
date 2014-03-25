# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TourConfig'
        db.create_table(u'tour_config_tourconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tour_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('tour_logo', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('tour_id', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
            ('tour_organization', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('dcs_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('gcm_sender_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('start_time', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('max_tour_time', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tour_route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tour_config.TourRoute'], null=True, on_delete=models.PROTECT, blank=True)),
            ('polling_rate', self.gf('django.db.models.fields.PositiveIntegerField')(default=600)),
        ))
        db.send_create_signal(u'tour_config', ['TourConfig'])

        # Adding model 'TourRoute'
        db.create_table(u'tour_config_tourroute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('route', self.gf('django.contrib.gis.db.models.fields.MultiLineStringField')()),
        ))
        db.send_create_signal(u'tour_config', ['TourRoute'])


    def backwards(self, orm):
        # Deleting model 'TourConfig'
        db.delete_table(u'tour_config_tourconfig')

        # Deleting model 'TourRoute'
        db.delete_table(u'tour_config_tourroute')


    models = {
        u'tour_config.tourconfig': {
            'Meta': {'object_name': 'TourConfig'},
            'dcs_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'gcm_sender_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_tour_time': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'polling_rate': ('django.db.models.fields.PositiveIntegerField', [], {'default': '600'}),
            'start_time': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tour_id': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'}),
            'tour_logo': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'tour_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'tour_organization': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'tour_route': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tour_config.TourRoute']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'})
        },
        u'tour_config.tourroute': {
            'Meta': {'object_name': 'TourRoute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'route': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {})
        }
    }

    complete_apps = ['tour_config']