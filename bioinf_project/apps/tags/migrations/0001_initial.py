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
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('wiki_page', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wiki.Page'], unique=True)),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['tags.Tag'])),
            ('node_position', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('categories', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'tags', ['Tag'])

        # Adding model 'UserTag'
        db.create_table(u'tags_usertag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='usertags', to=orm['tags.Tag'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='usertags', to=orm['users.User'])),
            ('answer_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'tags', ['UserTag'])

        # Adding unique constraint on 'UserTag', fields ['tag', 'user']
        db.create_unique(u'tags_usertag', ['tag_id', 'user_id'])

        # Adding M2M table for field answers on 'UserTag'
        m2m_table_name = db.shorten_name(u'tags_usertag_answers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usertag', models.ForeignKey(orm[u'tags.usertag'], null=False)),
            ('replypost', models.ForeignKey(orm[u'posts.replypost'], null=False))
        ))
        db.create_unique(m2m_table_name, ['usertag_id', 'replypost_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'UserTag', fields ['tag', 'user']
        db.delete_unique(u'tags_usertag', ['tag_id', 'user_id'])

        # Deleting model 'Tag'
        db.delete_table(u'tags_tag')

        # Deleting model 'UserTag'
        db.delete_table(u'tags_usertag')

        # Removing M2M table for field answers on 'UserTag'
        db.delete_table(db.shorten_name(u'tags_usertag_answers'))


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
            'wiki_page': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wiki.Page']", 'unique': 'True'})
        },
        u'tags.usertag': {
            'Meta': {'unique_together': "(('tag', 'user'),)", 'object_name': 'UserTag'},
            'answer_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'answers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['posts.ReplyPost']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'usertags'", 'to': u"orm['tags.Tag']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'usertags'", 'to': u"orm['users.User']"})
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

    complete_apps = ['tags']