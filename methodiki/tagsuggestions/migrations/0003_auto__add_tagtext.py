# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TagText'
        db.create_table('tagsuggestions_tagtext', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tagsuggestions.TagSuggestion'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
        ))
        db.send_create_signal('tagsuggestions', ['TagText'])


    def backwards(self, orm):
        
        # Deleting model 'TagText'
        db.delete_table('tagsuggestions_tagtext')


    models = {
        'tagsuggestions.tagsuggestion': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'TagSuggestion'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tagsuggestions.TagSuggestionCategory']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'show_on_frontpage': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
        },
        'tagsuggestions.tagsuggestioncategory': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'TagSuggestionCategory'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'tagsuggestions.tagtext': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'TagText'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tagsuggestions.TagSuggestion']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['tagsuggestions']
