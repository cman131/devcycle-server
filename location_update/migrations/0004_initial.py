# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'location_update_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('coords', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('speed', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.BigIntegerField')()),
            ('accuracy', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
            ('rider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rider.Rider'])),
            ('battery', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
            ('provider', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, blank=True)),
            ('bearing', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
            ('tour_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tour_config.TourConfig'], to_field='tour_id', on_delete=models.PROTECT)),
        ))
        db.send_create_signal(u'location_update', ['Location'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table(u'location_update_location')


    models = {
        u'location_update.location': {
            'Meta': {'object_name': 'Location'},
            'accuracy': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'battery': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'bearing': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'coords': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'blank': 'True'}),
            'rider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rider.Rider']"}),
            'speed': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.BigIntegerField', [], {}),
            'tour_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tour_config.TourConfig']", 'to_field': "'tour_id'", 'on_delete': 'models.PROTECT'})
        },
        u'rider.rider': {
            'Meta': {'object_name': 'Rider'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '125', 'null': 'True', 'blank': 'True'}),
            'push_id': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'registered_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
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

    complete_apps = ['location_update']