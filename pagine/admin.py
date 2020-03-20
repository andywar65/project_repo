from django.contrib import admin
from .models import ( HomePage, Institutional)

@admin.register(Institutional)
class InstitutionalAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('intro', )
