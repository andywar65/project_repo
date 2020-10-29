from django.contrib import admin

from .models import ( UserUpload, Article )
from .forms import ArticleForm
from pages.admin import GalleryImageInline

class UserUploadInline(admin.TabularInline):
    model = UserUpload
    fields = ('user', 'date', 'image', 'body', )
    extra = 0

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author', 'notice', )
    search_fields = ('title', 'date', 'intro', )
    inlines = [ GalleryImageInline, UserUploadInline,  ]
    form = ArticleForm

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/js/tinymce_setup.js',
        ]

    fieldsets = (
        (None, {
            'fields': ('title', 'date', 'intro'),
        }),
        ('Testo', {
            'classes': ('grp-collapse grp-closed', ),
            'fields': ('body', ),
        }),
        (None, {
            'fields': ('author', 'tags', 'notice'),
        }),
        )
