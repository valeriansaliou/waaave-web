# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Comment', fields ['is_active']
        db.create_index(u'notification_comment', ['is_active'])

        # Adding index on 'Comment', fields ['is_new']
        db.create_index(u'notification_comment', ['is_new'])

        # Adding index on 'Follow', fields ['is_active']
        db.create_index(u'notification_follow', ['is_active'])

        # Adding index on 'Follow', fields ['is_new']
        db.create_index(u'notification_follow', ['is_new'])

        # Adding index on 'Waaave', fields ['is_active']
        db.create_index(u'notification_waaave', ['is_active'])

        # Adding index on 'Waaave', fields ['is_new']
        db.create_index(u'notification_waaave', ['is_new'])

        # Adding index on 'FollowAdd', fields ['is_active']
        db.create_index(u'notification_followadd', ['is_active'])

        # Adding index on 'FollowAdd', fields ['is_new']
        db.create_index(u'notification_followadd', ['is_new'])


    def backwards(self, orm):
        # Removing index on 'FollowAdd', fields ['is_new']
        db.delete_index(u'notification_followadd', ['is_new'])

        # Removing index on 'FollowAdd', fields ['is_active']
        db.delete_index(u'notification_followadd', ['is_active'])

        # Removing index on 'Waaave', fields ['is_new']
        db.delete_index(u'notification_waaave', ['is_new'])

        # Removing index on 'Waaave', fields ['is_active']
        db.delete_index(u'notification_waaave', ['is_active'])

        # Removing index on 'Follow', fields ['is_new']
        db.delete_index(u'notification_follow', ['is_new'])

        # Removing index on 'Follow', fields ['is_active']
        db.delete_index(u'notification_follow', ['is_active'])

        # Removing index on 'Comment', fields ['is_new']
        db.delete_index(u'notification_comment', ['is_new'])

        # Removing index on 'Comment', fields ['is_active']
        db.delete_index(u'notification_comment', ['is_active'])


    models = {
        u'_index.ids': {
            'Meta': {'object_name': 'Ids'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_id': ('_commons.fields.IdField', [], {'db_index': 'True'}),
            'item_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'})
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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
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
        u'comment.active': {
            'Meta': {'object_name': 'Active'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comment_active_author'", 'to': u"orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hidden_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_reply_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comment_active_reply'", 'null': 'True', 'to': u"orm['comment.Active']"}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['_index.Ids']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'notification.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notification_comment_comment'", 'to': u"orm['comment.Active']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'is_new': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notification_comment_user'", 'to': u"orm['auth.User']"})
        },
        u'notification.follow': {
            'Meta': {'object_name': 'Follow'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'follow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notification_follow_follow'", 'to': u"orm['share.Follow']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'is_new': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notification_follow_user'", 'to': u"orm['auth.User']"})
        },
        u'notification.followadd': {
            'Meta': {'object_name': 'FollowAdd'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notification_followadd_index'", 'to': u"orm['_index.Ids']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'is_new': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notification_followadd_user'", 'to': u"orm['auth.User']"})
        },
        u'notification.waaave': {
            'Meta': {'object_name': 'Waaave'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'is_new': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notification_waaave_user'", 'to': u"orm['auth.User']"}),
            'waaave': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notification_waaave_waaave'", 'to': u"orm['share.Waaave']"})
        },
        u'share.follow': {
            'Meta': {'object_name': 'Follow'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'follower': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'follow_follower'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'share.waaave': {
            'Meta': {'object_name': 'Waaave'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['_index.Ids']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'waaave_user'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['notification']