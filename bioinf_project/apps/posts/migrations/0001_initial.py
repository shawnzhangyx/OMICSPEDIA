# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MainPostRevision'
        db.create_table(u'posts_mainpostrevision', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('revision_number', self.gf('django.db.models.fields.IntegerField')()),
            ('revision_summary', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['posts.MainPost'])),
        ))
        db.send_create_signal(u'posts', ['MainPostRevision'])

        # Adding model 'ReplyPostRevision'
        db.create_table(u'posts_replypostrevision', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('revision_number', self.gf('django.db.models.fields.IntegerField')()),
            ('revision_summary', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['posts.ReplyPost'])),
        ))
        db.send_create_signal(u'posts', ['ReplyPostRevision'])

        # Adding model 'MainPost'
        db.create_table(u'posts_mainpost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vote_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('current_revision', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='revision_post', unique=True, null=True, to=orm['posts.MainPostRevision'])),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('view_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('reply_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('bookmark_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('accepted_answer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='accepted_root', null=True, to=orm['posts.ReplyPost'])),
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
            ('vote_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('mainpost', self.gf('django.db.models.fields.related.ForeignKey')(related_name='replies', to=orm['posts.MainPost'])),
            ('current_revision', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='revision_post', unique=True, null=True, to=orm['posts.ReplyPostRevision'])),
            ('best_answer', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'posts', ['ReplyPost'])

        # Adding model 'MainPostComment'
        db.create_table(u'posts_mainpostcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=600)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['posts.MainPost'])),
        ))
        db.send_create_signal(u'posts', ['MainPostComment'])

        # Adding model 'ReplyPostComment'
        db.create_table(u'posts_replypostcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=600)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['posts.ReplyPost'])),
        ))
        db.send_create_signal(u'posts', ['ReplyPostComment'])


    def backwards(self, orm):
        # Deleting model 'MainPostRevision'
        db.delete_table(u'posts_mainpostrevision')

        # Deleting model 'ReplyPostRevision'
        db.delete_table(u'posts_replypostrevision')

        # Deleting model 'MainPost'
        db.delete_table(u'posts_mainpost')

        # Removing M2M table for field tags on 'MainPost'
        db.delete_table(db.shorten_name(u'posts_mainpost_tags'))

        # Deleting model 'ReplyPost'
        db.delete_table(u'posts_replypost')

        # Deleting model 'MainPostComment'
        db.delete_table(u'posts_mainpostcomment')

        # Deleting model 'ReplyPostComment'
        db.delete_table(u'posts_replypostcomment')


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
        u'posts.mainpost': {
            'Meta': {'object_name': 'MainPost'},
            'accepted_answer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'accepted_root'", 'null': 'True', 'to': u"orm['posts.ReplyPost']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'bookmark_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'current_revision': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'revision_post'", 'unique': 'True', 'null': 'True', 'to': u"orm['posts.MainPostRevision']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'reply_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'posts'", 'blank': 'True', 'to': u"orm['tags.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'view_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vote_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'posts.mainpostcomment': {
            'Meta': {'object_name': 'MainPostComment'},
            'content': ('django.db.models.fields.TextField', [], {'max_length': '600'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['posts.MainPost']"})
        },
        u'posts.mainpostrevision': {
            'Meta': {'object_name': 'MainPostRevision'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['posts.MainPost']"}),
            'revision_number': ('django.db.models.fields.IntegerField', [], {}),
            'revision_summary': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'posts.replypost': {
            'Meta': {'object_name': 'ReplyPost'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'best_answer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'current_revision': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'revision_post'", 'unique': 'True', 'null': 'True', 'to': u"orm['posts.ReplyPostRevision']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'mainpost': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'replies'", 'to': u"orm['posts.MainPost']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vote_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'posts.replypostcomment': {
            'Meta': {'object_name': 'ReplyPostComment'},
            'content': ('django.db.models.fields.TextField', [], {'max_length': '600'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['posts.ReplyPost']"})
        },
        u'posts.replypostrevision': {
            'Meta': {'object_name': 'ReplyPostRevision'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['posts.ReplyPost']"}),
            'revision_number': ('django.db.models.fields.IntegerField', [], {}),
            'revision_summary': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'tags.tag': {
            'Meta': {'object_name': 'Tag'},
            'categories': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'node_position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['tags.Tag']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tool_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'bookmark_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comment_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'current_revision': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'revision_page'", 'unique': 'True', 'null': 'True', 'to': u"orm['wiki.PageRevision']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'pages'", 'blank': 'True', 'to': u"orm['tags.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'view_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'wiki.pagerevision': {
            'Meta': {'object_name': 'PageRevision'},
            'added_chars': ('django.db.models.fields.IntegerField', [], {}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'deleted_chars': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'all_revisions'", 'to': u"orm['wiki.Page']"}),
            'revision_number': ('django.db.models.fields.IntegerField', [], {}),
            'revision_summary': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'total_chars': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['posts']