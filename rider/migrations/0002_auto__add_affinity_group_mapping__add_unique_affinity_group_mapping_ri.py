# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Affinity_Group_Mapping'
        db.create_table(u'rider_affinity_group_mapping', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rider.Rider'])),
            ('affinity_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['affinity.Group'])),
        ))
        db.send_create_signal(u'rider', ['Affinity_Group_Mapping'])

        # Adding unique constraint on 'Affinity_Group_Mapping', fields ['rider', 'affinity_group']
        db.create_unique(u'rider_affinity_group_mapping', ['rider_id', 'affinity_group_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Affinity_Group_Mapping', fields ['rider', 'affinity_group']
        db.delete_unique(u'rider_affinity_group_mapping', ['rider_id', 'affinity_group_id'])

        # Deleting model 'Affinity_Group_Mapping'
        db.delete_table(u'rider_affinity_group_mapping')


    models = {
        u'affinity.group': {
            'Meta': {'object_name': 'Group'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '7'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'registered_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'rider.affinity_group_mapping': {
            'Meta': {'unique_together': "(('rider', 'affinity_group'),)", 'object_name': 'Affinity_Group_Mapping'},
            'affinity_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['affinity.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rider.Rider']"})
        },
        u'rider.rider': {
            'Meta': {'object_name': 'Rider'},
            'affinity_group': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['affinity.Group']", 'through': u"orm['rider.Affinity_Group_Mapping']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '125', 'null': 'True', 'blank': 'True'}),
            'push_id': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'registered_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['rider']

