from django.contrib import admin
from .models import ( UserUpload, Blog, HomePage, Institutional)
from .forms import BlogForm

class UserUploadInline(admin.TabularInline):
    model = UserUpload
    fields = ('user', 'date', 'image', 'body', )
    extra = 0

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author', 'notice', )
    search_fields = ('title', 'date', 'intro', )
    inlines = [ UserUploadInline,  ]
    form = BlogForm

@admin.register(Institutional)
class InstitutionalAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('intro', )
