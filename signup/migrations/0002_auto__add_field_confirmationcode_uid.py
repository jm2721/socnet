# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ConfirmationCode.uid'
        db.add_column(u'signup_confirmationcode', 'uid',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=128),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ConfirmationCode.uid'
        db.delete_column(u'signup_confirmationcode', 'uid')


    models = {
        u'signup.confirmationcode': {
            'Meta': {'object_name': 'ConfirmationCode'},
            'code': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uid': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '128'})
        }
    }

    complete_apps = ['signup']