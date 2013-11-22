# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Like'
        db.delete_table(u'likes_like')


    def backwards(self, orm):
        # Adding model 'Like'
        db.create_table(u'likes_like', (
            ('linked_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.WallPost'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('liked_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
        ))
        db.send_create_signal(u'likes', ['Like'])


    models = {
        
    }

    complete_apps = ['likes']