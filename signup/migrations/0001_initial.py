# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ConfirmationCode'
        db.create_table(u'signup_confirmationcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.TextField')(max_length=128)),
        ))
        db.send_create_signal(u'signup', ['ConfirmationCode'])


    def backwards(self, orm):
        # Deleting model 'ConfirmationCode'
        db.delete_table(u'signup_confirmationcode')


    models = {
        u'signup.confirmationcode': {
            'Meta': {'object_name': 'ConfirmationCode'},
            'code': ('django.db.models.fields.TextField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['signup']