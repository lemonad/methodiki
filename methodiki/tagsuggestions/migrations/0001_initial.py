# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TagSuggestionCategory'
        db.create_table('tagsuggestions_tagsuggestioncategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
        ))
        db.send_create_signal('tagsuggestions', ['TagSuggestionCategory'])

        # Adding model 'TagSuggestion'
        db.create_table('tagsuggestions_tagsuggestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tagsuggestions.TagSuggestionCategory'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
        ))
        db.send_create_signal('tagsuggestions', ['TagSuggestion'])


    def backwards(self, orm):
        
        # Deleting model 'TagSuggestionCategory'
        db.delete_table('tagsuggestions_tagsuggestioncategory')

        # Deleting model 'TagSuggestion'
        db.delete_table('tagsuggestions_tagsuggestion')


    models = {
        'tagsuggestions.tagsuggestion': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'TagSuggestion'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tagsuggestions.TagSuggestionCategory']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'tagsuggestions.tagsuggestioncategory': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'TagSuggestionCategory'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['tagsuggestions']
