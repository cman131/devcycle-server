# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
	# Drop the Foreign Key constraint temporarily
	db.drop_foreign_key(u'rider_affinity_group_mapping', 'rider_id')
        
	# Changing field 'Rider.id'
        db.alter_column(u'rider_rider', 'id', self.gf('django.db.models.fields.CharField')(max_length=64, primary_key=True))
 
	# Changing field 'Rider.Affinity_Group_Mapping.id'
	db.alter_column(u'rider_affinity_group_mapping', 'rider_id',
                        self.gf('django.db.models.fields.related.ForeignKey')(
                            to=orm['rider.Rider']
                        ))

    def backwards(self, orm):
	# Drop the Foreign Key constraint temporarily
	db.drop_foreign_key(u'rider_affinity_group_mapping', 'rider_id')
        
        # Changing field 'Rider.id'
        db.alter_column(u'rider_rider', 'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))

	# Changing field 'Rider.Affinity_Group_Mapping.id'
	db.alter_column(u'rider_affinity_group_mapping', 'rider_id',
                        self.gf('django.db.models.fields.related.ForeignKey')(
                            to=orm['rider.Rider']
                        ))


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
            'id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '125', 'null': 'True', 'blank': 'True'}),
            'push_id': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'registered_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['rider']
