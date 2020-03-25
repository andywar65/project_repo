from django.contrib import admin
from .models import ( UserUpload, Article )
from .forms import ArticleForm

class UserUploadInline(admin.TabularInline):
    model = UserUpload
    fields = ('user', 'date', 'image', 'body', )
    extra = 0

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author', 'notice', )
    search_fields = ('title', 'date', 'intro', )
    inlines = [ UserUploadInline,  ]
    form = ArticleForm

    fieldsets = (
        ('Galleria', {
            'classes': ('collapse',),
            'fields': ('carousel', ),
        }),
        (None, {
            'fields': ('title', 'date', 'intro'),
        }),
        ('Testo', {
            'classes': ('collapse', 'wide'),
            'fields': ('stream', ),
        }),
        (None, {
            'fields': ('author', 'tags', 'notice'),
        }),
        )
