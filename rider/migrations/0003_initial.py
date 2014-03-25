# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rider'
        db.create_table(u'rider_rider', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('os', self.gf('django.db.models.fields.CharField')(max_length=125, null=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('push_id', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('registered_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'rider', ['Rider'])


    def backwards(self, orm):
        # Deleting model 'Rider'
        db.delete_table(u'rider_rider')


    models = {
        u'rider.rider': {
            'Meta': {'object_name': 'Rider'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '125', 'null': 'True', 'blank': 'True'}),
            'push_id': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'registered_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['rider']