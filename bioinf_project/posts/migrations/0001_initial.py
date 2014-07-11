# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MainPost'
        db.create_table(u'posts_mainpost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(default='Enter here')),
            ('vote_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('answered', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'posts', ['MainPost'])

        # Adding M2M table for field tags on 'MainPost'
        m2m_table_name = db.shorten_name(u'posts_mainpost_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mainpost', models.ForeignKey(orm[u'posts.mainpost'], null=False)),
            ('tag', models.ForeignKey(orm[u'tags.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['mainpost_id', 'tag_id'])

        # Adding model 'ReplyPost'
        db.create_table(u'posts_replypost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(default='Enter here')),
            ('vote_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('root', self.gf('django.db.models.fields.related.ForeignKey')(related_name='replies', to=orm['posts.MainPost'])),
        ))
        db.send_create_signal(u'posts', ['ReplyPost'])

        # Adding M2M table for field tags on 'ReplyPost'
        m2m_table_name = db.shorten_name(u'posts_replypost_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('replypost', models.ForeignKey(orm[u'posts.replypost'], null=False)),
            ('tag', models.ForeignKey(orm[u'tags.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['replypost_id', 'tag_id'])


    def backwards(self, orm):
        # Deleting model 'MainPost'
        db.delete_table(u'posts_mainpost')

        # Removing M2M table for field tags on 'MainPost'
        db.delete_table(db.shorten_name(u'posts_mainpost_tags'))

        # Deleting model 'ReplyPost'
        db.delete_table(u'posts_replypost')

        # Removing M2M table for field tags on 'ReplyPost'
        db.delete_table(db.shorten_name(u'posts_replypost_tags'))


    models = {
        u'posts.mainpost': {
            'Meta': {'object_name': 'MainPost'},
            'answered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "'Enter here'"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tags.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vote_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'posts.replypost': {
            'Meta': {'object_name': 'ReplyPost'},
            'content': ('django.db.models.fields.TextField', [], {'default': "'Enter here'"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'replies'", 'to': u"orm['posts.MainPost']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tags.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'vote_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
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

    complete_apps = ['posts']