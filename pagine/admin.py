from django.contrib import admin
from django.conf import settings
from users.models import Member
from .models import ( Location, Event, EventUpgrade, UserUpload, Blog)
from .forms import EventForm, BlogForm
from rpnew_prog.utils import send_rp_mail

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'get_gmap_link')
    readonly_fields = ('slug', )
    search_fields = ('title', 'address')

class EventUpgradeInline(admin.TabularInline):
    model = EventUpgrade
    fields = ('title', 'date', 'body', )
    extra = 0

class UserUploadInline(admin.TabularInline):
    model = UserUpload
    fields = ('user', 'date', 'image', 'body', )
    extra = 0

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'notice')
    inlines = [ UserUploadInline ]
    search_fields = ('title', 'date', 'intro', )
    form = EventForm
    actions = ['send_notice', ]
    autocomplete_fields = ['location', ]

    def send_notice(self, request, queryset):
        for event in queryset:
            message = event.title + '\n'
            upgrades = EventUpgrade.objects.filter(event_id=event.id)
            if upgrades:
                upgrade = upgrades[0]
                message += upgrade.body + '\n'
            message += event.intro + '\n'
            url = settings.BASE_URL + event.get_path()
            message += 'Fai click su questo link: ' + url + '\n'
            recipients = Member.objects.filter(parent = None,
                user__is_active = True, no_spam = True, )
            mailto = []
            for recipient in recipients:
                mailto.append(recipient.email)
            subject = 'Nuovo appuntamento / aggiornamento RP'
            send_rp_mail(subject, message, mailto)
            event.notice = 'DONE'
            event.save()
    send_notice.short_description = 'Invia notifiche'

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'intro', 'date', 'author', )
    search_fields = ('title', 'date', 'intro', )
    inlines = [ UserUploadInline,  ]
    form = BlogForm
    #autocomplete_fields = ['image', ]
