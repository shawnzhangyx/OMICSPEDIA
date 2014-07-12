# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Page'
        db.create_table(u'wiki_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'wiki', ['Page'])

        # Adding M2M table for field tags on 'Page'
        m2m_table_name = db.shorten_name(u'wiki_page_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('page', models.ForeignKey(orm[u'wiki.page'], null=False)),
            ('tag', models.ForeignKey(orm[u'tags.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['page_id', 'tag_id'])

        # Adding model 'Section'
        db.create_table(u'wiki_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'wiki', ['Section'])


    def backwards(self, orm):
        # Deleting model 'Page'
        db.delete_table(u'wiki_page')

        # Removing M2M table for field tags on 'Page'
        db.delete_table(db.shorten_name(u'wiki_page_tags'))

        # Deleting model 'Section'
        db.delete_table(u'wiki_section')


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
        },
        u'wiki.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tags.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'wiki.section': {
            'Meta': {'object_name': 'Section'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section_title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['wiki']