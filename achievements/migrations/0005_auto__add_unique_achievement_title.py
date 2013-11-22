# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field achieved_by on 'Achievement'
        db.delete_table(db.shorten_name(u'achievements_achievement_achieved_by'))

        # Adding unique constraint on 'Achievement', fields ['title']
        db.create_unique(u'achievements_achievement', ['title'])


    def backwards(self, orm):
        # Removing unique constraint on 'Achievement', fields ['title']
        db.delete_unique(u'achievements_achievement', ['title'])

        # Adding M2M table for field achieved_by on 'Achievement'
        m2m_table_name = db.shorten_name(u'achievements_achievement_achieved_by')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('achievement', models.ForeignKey(orm[u'achievements.achievement'], null=False)),
            ('user', models.ForeignKey(orm[u'users.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['achievement_id', 'user_id'])


    models = {
        u'achievements.achievement': {
            'Meta': {'object_name': 'Achievement'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'ach title'", 'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['achievements']