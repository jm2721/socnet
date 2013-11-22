# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ConfirmationCode.code'
        db.alter_column(u'signup_confirmationcode', 'code', self.gf('django.db.models.fields.CharField')(max_length=128))

        # Changing field 'ConfirmationCode.uid'
        db.alter_column(u'signup_confirmationcode', 'uid', self.gf('django.db.models.fields.CharField')(max_length=128))

    def backwards(self, orm):

        # Changing field 'ConfirmationCode.code'
        db.alter_column(u'signup_confirmationcode', 'code', self.gf('django.db.models.fields.TextField')(max_length=128))

        # Changing field 'ConfirmationCode.uid'
        db.alter_column(u'signup_confirmationcode', 'uid', self.gf('django.db.models.fields.TextField')(max_length=128))

    models = {
        u'signup.confirmationcode': {
            'Meta': {'object_name': 'ConfirmationCode'},
            'code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'})
        }
    }

    complete_apps = ['signup']