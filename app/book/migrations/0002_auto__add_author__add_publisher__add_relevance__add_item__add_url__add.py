# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table(u'book_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['book.Item'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['book.Person'])),
        ))
        db.send_create_signal(u'book', ['Author'])

        # Adding model 'Publisher'
        db.create_table(u'book_publisher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'book', ['Publisher'])

        # Adding model 'Relevance'
        db.create_table(u'book_relevance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'book_relevance_related', to=orm['auth.User'])),
            ('is_relevant', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['book.Item'])),
        ))
        db.send_create_signal(u'book', ['Relevance'])

        # Adding model 'Item'
        db.create_table(u'book_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('description', self.gf('bbcode.fields.BBCodeTextField')()),
            ('pages', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('isbn', self.gf('_commons.fields.ISBNField')(max_length=13)),
            ('language', self.gf('_commons.fields.LanguageField')(default='en-us', max_length=5)),
            ('is_visible', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('amazon_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('date_release', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'book', ['Item'])

        # Adding model 'Url'
        db.create_table(u'book_url', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['book.Item'])),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=140, db_index=True)),
            ('is_alias', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal(u'book', ['Url'])

        # Adding model 'Tag'
        db.create_table(u'book_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'book_tag_related', to=orm['tag.List'])),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['book.Item'])),
        ))
        db.send_create_signal(u'book', ['Tag'])

        # Adding model 'Person'
        db.create_table(u'book_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'book', ['Person'])


    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table(u'book_author')

        # Deleting model 'Publisher'
        db.delete_table(u'book_publisher')

        # Deleting model 'Relevance'
        db.delete_table(u'book_relevance')

        # Deleting model 'Item'
        db.delete_table(u'book_item')

        # Deleting model 'Url'
        db.delete_table(u'book_url')

        # Deleting model 'Tag'
        db.delete_table(u'book_tag')

        # Deleting model 'Person'
        db.delete_table(u'book_person')


    models = {
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
        u'book.author': {
            'Meta': {'object_name': 'Author'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['book.Item']"}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['book.Person']"})
        },
        u'book.item': {
            'Meta': {'object_name': 'Item'},
            'amazon_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_release': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('bbcode.fields.BBCodeTextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'isbn': ('_commons.fields.ISBNField', [], {'max_length': '13'}),
            'language': ('_commons.fields.LanguageField', [], {'default': "'en-us'", 'max_length': '5'}),
            'pages': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        u'book.person': {
            'Meta': {'object_name': 'Person'},
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'book.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'book.relevance': {
            'Meta': {'object_name': 'Relevance'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['book.Item']"}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_relevant': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'book_relevance_related'", 'to': u"orm['auth.User']"})
        },
        u'book.tag': {
            'Meta': {'object_name': 'Tag'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['book.Item']"}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'book_tag_related'", 'to': u"orm['tag.List']"})
        },
        u'book.url': {
            'Meta': {'object_name': 'Url'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['book.Item']"}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_alias': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '140', 'db_index': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tag.list': {
            'Meta': {'object_name': 'List'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'})
        }
    }

    complete_apps = ['book']