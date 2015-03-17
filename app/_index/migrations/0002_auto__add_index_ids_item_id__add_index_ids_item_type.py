# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Ids', fields ['item_id']
        db.create_index(u'_index_ids', ['item_id'])

        # Adding index on 'Ids', fields ['item_type']
        db.create_index(u'_index_ids', ['item_type'])


    def backwards(self, orm):
        # Removing index on 'Ids', fields ['item_type']
        db.delete_index(u'_index_ids', ['item_type'])

        # Removing index on 'Ids', fields ['item_id']
        db.delete_index(u'_index_ids', ['item_id'])


    models = {
        u'_index.ids': {
            'Meta': {'object_name': 'Ids'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_id': ('_commons.fields.IdField', [], {'db_index': 'True'}),
            'item_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['_index']