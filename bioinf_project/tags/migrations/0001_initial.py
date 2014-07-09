# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'tags_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['tags.Tag'])),
            ('sibling_before', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='after', null=True, to=orm['tags.Tag'])),
            ('sibling_after', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='before', null=True, to=orm['tags.Tag'])),
            ('categories', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'tags', ['Tag'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'tags_tag')


    models = {
        u'tags.tag': {
            'Meta': {'object_name': 'Tag'},
            'categories': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['tags.Tag']"}),
            'sibling_after': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'before'", 'null': 'True', 'to': u"orm['tags.Tag']"}),
            'sibling_before': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'after'", 'null': 'True', 'to': u"orm['tags.Tag']"})
        }
    }

    complete_apps = ['tags']