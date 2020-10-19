from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import ( HomePage, TreePage )

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('__str__', )

    fieldsets = (
        ('Galleria', {
            'classes': ('collapse',),
            'fields': ('carousel', ),
        }),
        (None, {
            'fields': ('intro', 'body', 'action'),
        }),
        )

    #class Media:
        #js = [
            #'/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            #'/static/js/tinymce_setup.js',
        #]

class TreePageAdmin(TreeAdmin):
    form = movenodeform_factory(TreePage)

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'intro'),
        }),
        ('Testo', {
            'classes': ('collapse', 'wide'),
            'fields': ('stream', ),
        }),
        (None, {
            'fields': ('summary', 'navigation'),
        }),
        (None, {
            'fields': ('_position', '_ref_node_id'),
        }),
        )

admin.site.register(TreePage, TreePageAdmin)
