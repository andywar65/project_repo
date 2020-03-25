from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import ( HomePage, TreePage )

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('intro', )

    fieldsets = (
        ('Galleria', {
            'classes': ('collapse',),
            'fields': ('carousel', ),
        }),
        (None, {
            'fields': ('intro', 'action'),
        }),
        )

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
        )

admin.site.register(TreePage, TreePageAdmin)
