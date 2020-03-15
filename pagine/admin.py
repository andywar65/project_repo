from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import admin
from .models import ( UserUpload, Blog, HomePage, Institutional)
from .forms import BlogForm
from users.models import Profile

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
    #actions = ['send_notice', ]

    def send_notice(self, request, queryset):
        for post in queryset:
            message = post.title + '\n'
            message += post.intro + '\n'
            url = settings.BASE_URL + post.get_path()
            message += 'Fai click su questo link per leggerlo: ' + url + '\n'
            recipients = Profile.objects.filter(
                user__is_active = True, no_spam = True, )
            mailto = []
            for recipient in recipients:
                mailto.append(recipient.user.email)
            subject = 'Nuovo articolo'
            email = EmailMessage(subject, message, settings.SERVER_EMAIL,
                [mailto])
            email.send()
            post.notice = 'DONE'
            post.save()
    send_notice.short_description = 'Invia notifiche'

@admin.register(Institutional)
class InstitutionalAdmin(admin.ModelAdmin):
    list_display = ('title', 'type')

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('intro', )
