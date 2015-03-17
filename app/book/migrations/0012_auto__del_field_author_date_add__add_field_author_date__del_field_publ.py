# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Author.date_add'
        db.delete_column(u'book_author', 'date_add')

        # Adding field 'Author.date'
        db.add_column(u'book_author', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 12, 6, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Publisher.date_add'
        db.delete_column(u'book_publisher', 'date_add')

        # Adding field 'Publisher.date'
        db.add_column(u'book_publisher', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 12, 6, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'House.date_add'
        db.delete_column(u'book_house', 'date_add')

        # Adding field 'House.date'
        db.add_column(u'book_house', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 12, 6, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Item.date_add'
        db.delete_column(u'book_item', 'date_add')

        # Adding field 'Item.date'
        db.add_column(u'book_item', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 12, 6, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Url.date_add'
        db.delete_column(u'book_url', 'date_add')

        # Adding field 'Url.date'
        db.add_column(u'book_url', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 12, 6, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Tag.date_add'
        db.delete_column(u'book_tag', 'date_add')

        # Adding field 'Tag.date'
        db.add_column(u'book_tag', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 12, 6, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Person.date_add'
        db.delete_column(u'book_person', 'date_add')

        # Adding field 'Person.date'
        db.add_column(u'book_person', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 12, 6, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Author.date_add'
        db.add_column(u'book_author', 'date_add',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 12, 6, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Author.date'
        db.delete_column(u'book_author', 'date')

        # Adding field 'Publisher.date_add'
        db.add_column(u'book_publisher', 'date_add',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 12, 6, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Publisher.date'
        db.delete_column(u'book_publisher', 'date')

        # Adding field 'House.date_add'
        db.add_column(u'book_house', 'date_add',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 12, 6, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'House.date'
        db.delete_column(u'book_house', 'date')

        # Adding field 'Item.date_add'
        db.add_column(u'book_item', 'date_add',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 12, 6, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Item.date'
        db.delete_column(u'book_item', 'date')

        # Adding field 'Url.date_add'
        db.add_column(u'book_url', 'date_add',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 12, 6, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Url.date'
        db.delete_column(u'book_url', 'date')

        # Adding field 'Tag.date_add'
        db.add_column(u'book_tag', 'date_add',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 12, 6, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Tag.date'
        db.delete_column(u'book_tag', 'date')

        # Adding field 'Person.date_add'
        db.add_column(u'book_person', 'date_add',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 12, 6, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Person.date'
        db.delete_column(u'book_person', 'date')


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
            'book': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['book.Item']", 'unique': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['book.Person']", 'unique': 'True'})
        },
        u'book.house': {
            'Meta': {'object_name': 'House'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'book.item': {
            'Meta': {'object_name': 'Item'},
            'amazon_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'cover_large': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'cover_medium': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'cover_original': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'cover_small': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_release': ('django.db.models.fields.DateTimeField', [], {}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('bbcode.fields.BBCodeTextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'isbn': ('_commons.fields.ISBNField', [], {'max_length': '13'}),
            'language': ('_commons.fields.LanguageField', [], {'default': "'en'", 'max_length': '2'}),
            'pages': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'db_index': 'True'})
        },
        u'book.person': {
            'Meta': {'object_name': 'Person'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'book.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'book': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['book.Item']", 'unique': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'house': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['book.House']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'book.tag': {
            'Meta': {'object_name': 'Tag'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'book_tags'", 'to': u"orm['book.Item']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'book_tag_list'", 'to': u"orm['tag.List']"})
        },
        u'book.url': {
            'Meta': {'object_name': 'Url'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['book.Item']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'picture_large': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'picture_normal': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'picture_original': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'picture_small': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'})
        }
    }

    complete_apps = ['book']