from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (User, Profile, UserMessage, )

class UserAdmin(UserAdmin):
    list_display = ('get_full_name', 'is_staff', 'is_active', 'is_superuser')
    list_editable = ('is_staff', 'is_active')

admin.site.register(User, UserAdmin)

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_email', 'subject', )
    ordering = ('-id', )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'is_trusted')
    list_editable = ('is_trusted', )
