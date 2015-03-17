# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table(u'account_profile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('specialty', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('freelancing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hiring', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rank', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('experience', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=19, decimal_places=2)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('facebook', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('github', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('dribbble', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('register_complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('identity_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('website_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'account', ['Profile'])

        # Adding model 'Settings'
        db.create_table(u'account_settings', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('email_respond', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('email_follow', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('email_follow_add', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notif_respond', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notif_follow', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notif_follow_add', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notif_waaave', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'account', ['Settings'])

        # Adding model 'Register'
        db.create_table(u'account_register', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('step_current', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('resumed_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('date_start', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_complete', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('ip_start', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('ip_update', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('ip_complete', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, null=True, blank=True)),
        ))
        db.send_create_signal(u'account', ['Register'])

        # Adding model 'Recover'
        db.create_table(u'account_recover', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('recovered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_generated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_recovered', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_expire', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('key_uidb36', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('key_token', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('key_random', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'account', ['Recover'])

        # Adding model 'Confirm'
        db.create_table(u'account_confirm', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_generated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_confirmed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('key_uidb36', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('key_token', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('key_random', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'account', ['Confirm'])


    def backwards(self, orm):
        # Deleting model 'Profile'
        db.delete_table(u'account_profile')

        # Deleting model 'Settings'
        db.delete_table(u'account_settings')

        # Deleting model 'Register'
        db.delete_table(u'account_register')

        # Deleting model 'Recover'
        db.delete_table(u'account_recover')

        # Deleting model 'Confirm'
        db.delete_table(u'account_confirm')


    models = {
        u'account.confirm': {
            'Meta': {'object_name': 'Confirm'},
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_confirmed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_generated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'key_random': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'key_token': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'key_uidb36': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'account.profile': {
            'Meta': {'object_name': 'Profile'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'dribbble': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'email_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'experience': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '19', 'decimal_places': '2'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'freelancing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'github': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'hiring': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'identity_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rank': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'register_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'specialty': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'website_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'account.recover': {
            'Meta': {'object_name': 'Recover'},
            'date_expire': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_generated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_recovered': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'key_random': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'key_token': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'key_uidb36': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'recovered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'account.register': {
            'Meta': {'object_name': 'Register'},
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_complete': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'ip_complete': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'null': 'True', 'blank': 'True'}),
            'ip_start': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'ip_update': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'resumed_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'step_current': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'account.settings': {
            'Meta': {'object_name': 'Settings'},
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email_follow': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email_follow_add': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email_respond': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notif_follow': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notif_follow_add': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notif_respond': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notif_waaave': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['account']