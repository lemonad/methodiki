# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'TagSuggestion.show_on_frontpage'
        db.add_column('tagsuggestions_tagsuggestion', 'show_on_frontpage', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'TagSuggestion.show_on_frontpage'
        db.delete_column('tagsuggestions_tagsuggestion', 'show_on_frontpage')


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
        }
    }

    complete_apps = ['tagsuggestions']
