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
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('current_revision', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='revision_page', unique=True, null=True, to=orm['wiki.PageRevision'])),
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

        # Adding model 'PageRevision'
        db.create_table(u'wiki_pagerevision', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('revision_number', self.gf('django.db.models.fields.IntegerField')()),
            ('revision_summary', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.Page'])),
            ('total_chars', self.gf('django.db.models.fields.IntegerField')()),
            ('added_chars', self.gf('django.db.models.fields.IntegerField')()),
            ('deleted_chars', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'wiki', ['PageRevision'])

        # Adding model 'PageComment'
        db.create_table(u'wiki_pagecomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('comment_type', self.gf('django.db.models.fields.IntegerField')(default='discuss')),
            ('issue', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('detail', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['wiki.Page'])),
            ('init_revision', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='comment_init', null=True, to=orm['wiki.PageRevision'])),
            ('final_revision', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='comment_closed', null=True, to=orm['wiki.PageRevision'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'wiki', ['PageComment'])


    def backwards(self, orm):
        # Deleting model 'Page'
        db.delete_table(u'wiki_page')

        # Removing M2M table for field tags on 'Page'
        db.delete_table(db.shorten_name(u'wiki_page_tags'))

        # Deleting model 'PageRevision'
        db.delete_table(u'wiki_pagerevision')

        # Deleting model 'PageComment'
        db.delete_table(u'wiki_pagecomment')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tags.tag': {
            'Meta': {'object_name': 'Tag'},
            'bookmark_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'categories': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'node_position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['tags.Tag']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'wiki_page': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'wiki_tag'", 'unique': 'True', 'to': u"orm['wiki.Page']"})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'email_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        },
        u'wiki.page': {
            'Meta': {'object_name': 'Page'},
            'current_revision': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'revision_page'", 'unique': 'True', 'null': 'True', 'to': u"orm['wiki.PageRevision']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'pages'", 'blank': 'True', 'to': u"orm['tags.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'wiki.pagecomment': {
            'Meta': {'object_name': 'PageComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'comment_type': ('django.db.models.fields.IntegerField', [], {'default': "'discuss'"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'detail': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'final_revision': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comment_closed'", 'null': 'True', 'to': u"orm['wiki.PageRevision']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'init_revision': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comment_init'", 'null': 'True', 'to': u"orm['wiki.PageRevision']"}),
            'issue': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['wiki.Page']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'wiki.pagerevision': {
            'Meta': {'object_name': 'PageRevision'},
            'added_chars': ('django.db.models.fields.IntegerField', [], {}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'deleted_chars': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wiki.Page']"}),
            'revision_number': ('django.db.models.fields.IntegerField', [], {}),
            'revision_summary': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'total_chars': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['wiki']