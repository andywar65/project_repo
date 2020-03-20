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
