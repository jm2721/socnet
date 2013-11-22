# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'ConfirmationCode', fields ['code', 'uid']
        db.create_unique(u'signup_confirmationcode', ['code', 'uid'])


    def backwards(self, orm):
        # Removing unique constraint on 'ConfirmationCode', fields ['code', 'uid']
        db.delete_unique(u'signup_confirmationcode', ['code', 'uid'])


    models = {
        u'signup.confirmationcode': {
            'Meta': {'unique_together': "(('code', 'uid'),)", 'object_name': 'ConfirmationCode'},
            'code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'})
        }
    }

    complete_apps = ['signup']