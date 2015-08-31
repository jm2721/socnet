# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Like'
        db.create_table(u'likes_like', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('linked_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.WallPost'])),
            ('liked_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
        ))
        db.send_create_signal(u'likes', ['Like'])

        # Adding unique constraint on 'Like', fields ['linked_to', 'liked_by']
        db.create_unique(u'likes_like', ['linked_to_id', 'liked_by_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Like', fields ['linked_to', 'liked_by']
        db.delete_unique(u'likes_like', ['linked_to_id', 'liked_by_id'])

        # Deleting model 'Like'
        db.delete_table(u'likes_like')


    models = {
        u'achievements.achievement': {
            'Meta': {'object_name': 'Achievement'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'ach title'", 'unique': 'True', 'max_length': '50'})
        },
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
        u'likes.like': {
            'Meta': {'unique_together': "(('linked_to', 'liked_by'),)", 'object_name': 'Like'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'liked_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'linked_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.WallPost']"})
        },
        u'users.user': {
            'Meta': {'ordering': "['id']", 'object_name': 'User'},
            'achievements': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['achievements.Achievement']", 'symmetrical': 'False'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'friends_rel_+'", 'null': 'True', 'to': u"orm['users.User']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'users.wallpost': {
            'Meta': {'object_name': 'WallPost'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'poster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'poster'", 'to': u"orm['users.User']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receiver'", 'to': u"orm['users.User']"})
        }
    }

    complete_apps = ['likes']