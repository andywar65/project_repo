from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import ( HomePage, GalleryImage, HomeButton, TreePage )

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    fields = ('fb_image', 'caption', 'position')
    sortable_field_name = "position"
    extra = 0

class HomeButtonInline(admin.TabularInline):
    model = HomeButton
    fields = ('title', 'subtitle', 'link', 'position')
    sortable_field_name = "position"
    extra = 0

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', )
    inlines = [ GalleryImageInline, HomeButtonInline,  ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/js/tinymce_setup.js',
        ]

class TreePageAdmin(TreeAdmin):
    form = movenodeform_factory(TreePage)

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/js/tinymce_setup.js',
        ]

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'intro'),
        }),
        ('Testo', {
            'classes': ('grp-collapse grp-closed', ),
            'fields': ('body', ),
        }),
        (None, {
            'fields': ('summary', 'navigation'),
        }),
        (None, {
            'fields': ('_position', '_ref_node_id'),
        }),
        )

admin.site.register(TreePage, TreePageAdmin)
