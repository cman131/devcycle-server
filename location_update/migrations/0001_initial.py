# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table('location_update_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('coords', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('speed', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.BigIntegerField')()),
            ('accuracy', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
            ('rider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rider.Rider'])),
            ('battery', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
            ('provider', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, blank=True)),
            ('bearing', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('location_update', ['Location'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table('location_update_location')


    models = {
        'location_update.location': {
            'Meta': {'object_name': 'Location'},
            'accuracy': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'battery': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'bearing': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'coords': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'blank': 'True'}),
            'rider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rider.Rider']"}),
            'speed': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.BigIntegerField', [], {})
        },
        'rider.rider': {
            'Meta': {'object_name': 'Rider'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '125', 'null': 'True', 'blank': 'True'}),
            'push_id': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'registered_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['location_update']