from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import ( HomePage, TreePage, Institutional)

@admin.register(Institutional)
class InstitutionalAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('intro', )

class TreePageAdmin(TreeAdmin):
    form = movenodeform_factory(TreePage)

admin.site.register(TreePage, TreePageAdmin)
