from datetime import date, timedelta
#from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.db.models import Q

from .models import (User, Member, MemberPayment, Applicant,
    ApplicantChild, UserMessage, CourseSchedule,)
from .forms import (ChangeMemberChildForm, ChangeMember0Form,
    ChangeMember1Form, ChangeMember2Form, ChangeMember3Form)
from project.utils import send_rp_mail

class UserAdmin(UserAdmin):
    list_display = ('username', 'is_staff', 'is_active', 'is_superuser')
    list_editable = ('is_staff', 'is_active')

admin.site.register(User, UserAdmin)

@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('full', 'abbrev')
    ordering = ('abbrev', )

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_email', 'subject', )
    ordering = ('-id', )

class ApplicantChildInline(admin.TabularInline):
    model = ApplicantChild
    fields = ('first_name', 'last_name', )
    extra = 0

def generate_unique_username(username):
    username = username.replace(' ', '_')
    unique_username = username
    numb = 1
    while User.objects.filter(username=unique_username).exists():
        unique_username = '%s_%d' % (username, numb)
        numb += 1
    return unique_username

def registration_message( name, username, password ):
    message = f"""
        Ciao {name}! \n
        Abbiamo ricevuto la tua registrazione al sito di Rifondazione
        Podistica. Puoi effettuare il Login al seguente link: \n
        {settings.BASE_URL}/accounts/login/ \n
        Usa questo nome utente: {username}
        e questa password: {password} (possibilmente da cambiare).
        Una volta effettuato il login potrai gestire il tuo profilo.
        Grazie.
        Lo staff di RP \n
        Link utili:
        Informativa per la privacy: {settings.BASE_URL}/privacy/
        Cambio password: {settings.BASE_URL}/accounts/password_change/
        """
    return message

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'sector', 'children_str',)
    ordering = ('last_name', 'first_name', )
    search = ('last_name', 'first_name', 'children_str',)
    inlines = [ ApplicantChildInline, ]
    actions = ['applicant_to_user', ]

    def applicant_to_user(self, request, queryset):
        for applicant in queryset:
            username = (applicant.last_name.lower() + '_' +
                applicant.first_name.lower())
            username = generate_unique_username(username)
            password = User.objects.make_random_password()
            hash_password = make_password(password)
            if not applicant.parent:
                usr = User.objects.create(username = username,
                    password = hash_password, is_staff = False, )
            else:
                password = 'rifondazionepodistica'
                hash_password = make_password( password )
                usr = User.objects.create(username = username,
                    password = hash_password, is_staff = False, )
            member = Member.objects.get(user_id=usr.id)
            member.sector = applicant.sector
            member.first_name = applicant.first_name
            member.last_name = applicant.last_name
            member.email = applicant.email
            member.no_spam = applicant.no_spam
            if applicant.parent:
                member.parent = applicant.parent
                member.sector = '1-YC'
                member.email = applicant.parent.member.email
                if member.parent.member.sector == '0-NO':
                    parent = Member.objects.get(pk=member.parent.id)
                    parent.sector = '3-FI'
                    parent.save()
            children = ApplicantChild.objects.filter(parent=applicant.id)
            if children and member.sector == '0-NO':
                member.sector = '3-FI'
            member.save()
            for child in children:
                chd_username = (child.last_name.lower() + '_' +
                    child.first_name.lower())
                chd_username = generate_unique_username(chd_username)
                hash_password = make_password('rifondazionepodistica')
                chd = User.objects.create(username = chd_username,
                    password = hash_password, )
                member = Member.objects.get(user_id=chd.id)
                member.sector = '1-YC'
                member.parent = usr
                member.first_name = child.first_name
                member.last_name = child.last_name
                member.email = applicant.email
                member.save()
            if not applicant.parent:
                mail_to = [applicant.email, ]
                message = registration_message( member.first_name, username,
                    password )
                subject = 'Credenziali di accesso ad RP'
                send_rp_mail(subject, message, mail_to)
            applicant.delete()
        return
    applicant_to_user.short_description = 'Crea Iscritti'

class MemberPaymentInline(admin.TabularInline):
    model = MemberPayment
    fields = ('date', 'amount')
    extra = 0

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('get_thumb', 'get_full_name', 'sector', 'parent',
        'mc_state', 'settled')
    list_filter = ('mc_state', 'settled')
    search_fields = ('first_name', 'last_name', 'fiscal_code', 'address')
    ordering = ('last_name', 'first_name', )
    actions = ['control_mc', 'reset_all', 'control_pay']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        member = Member.objects.get(user_id=object_id)
        if member.parent:
            self.form = ChangeMemberChildForm
            if not request.user.has_perm('users.add_applicant'):
                self.readonly_fields = ['sector', 'parent', 'membership',
                    'mc_expiry', 'mc_state', 'total_amount', 'settled']
            self.inlines = [ MemberPaymentInline, ]
        elif member.sector == '0-NO':
            self.form = ChangeMember0Form
            if not request.user.has_perm('users.add_applicant'):
                self.readonly_fields = ['sector', ]
        elif member.sector == '1-YC':
            self.form = ChangeMember1Form
            if not request.user.has_perm('users.add_applicant'):
                self.readonly_fields = ['sector', 'membership',
                    'mc_expiry', 'mc_state', 'total_amount', 'settled']
            self.inlines = [ MemberPaymentInline, ]
        elif member.sector == '2-NC':
            self.form = ChangeMember2Form
            if not request.user.has_perm('users.add_applicant'):
                self.readonly_fields = ['sector', 'membership',
                    'mc_expiry', 'mc_state', 'total_amount', 'settled']
            self.inlines = [ MemberPaymentInline, ]
        elif member.sector == '3-FI':
            self.form = ChangeMember3Form
            if not request.user.has_perm('users.add_applicant'):
                self.readonly_fields = ['sector', ]
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def control_mc(self, request, queryset):
        if not request.user.has_perm('users.add_applicant'):
            return
        else:
            for member in queryset:
                if member.sector == '0-NO':
                    continue
                if member.mc_state == None:
                    member.mc_state = '0-NF'
                    member.save()
                elif (member.mc_state == '0-NF' or
                    member.mc_state == '5-NI'):
                    if member.med_cert:
                        member.mc_state = '1-VF'
                        member.save()
                elif member.mc_state == '2-RE':
                    if member.mc_expiry<date.today() + timedelta(days=30):
                        member.mc_state = '6-IS'
                        member.save()
                    elif member.mc_expiry<date.today():
                        member.mc_state = '3-SV'
                        member.save()
                elif member.mc_state == '6-IS':
                    if member.mc_expiry<date.today():
                        member.mc_state = '3-SV'
                        member.save()
                elif member.mc_state == '4-SI':
                    member.med_cert = None
                    member.mc_expiry = None
                    member.mc_state = '5-NI'
                    member.save()
                    if member.parent:
                        mail_to = [member.parent.email, ]
                    else:
                        mail_to = [member.email, ]
                    message = 'Buongiorno \n'
                    message += f'Il CM/CMA di {member.get_full_name()} '
                    message += 'risulta scaduto o inesistente. \n'
                    message += 'Si prega di rimediare al più presto. Grazie. \n'
                    message += 'Lo staff di RP'
                    subject = 'Verifica CM/CMA'
                    send_rp_mail(subject, message, mail_to)
    control_mc.short_description = 'Gestisci CM/CMA'

    def reset_all(self, request, queryset):
        if not request.user.has_perm('users.add_applicant'):
            return
        queryset.update(sign_up='', privacy='', settled='', total_amount=0.00)
        for member in queryset:
            MemberPayment.objects.filter(member_id = member.pk).delete()
    reset_all.short_description = 'Resetta i dati'

    def control_pay(self, request, queryset):
        if not request.user.has_perm('users.add_applicant'):
            return
        for member in queryset:
            if member.sector == '0-NO' or member.settled == 'YES':
                continue
            elif member.total_amount == 0.00:
                member.settled = 'VI'
                member.save()
            else:
                paid = 0.00
                payments = MemberPayment.objects.filter(member_id = member.pk)
                for payment in payments:
                    paid += payment.amount
                if paid >= member.total_amount:
                    member.settled = 'YES'
                    member.save()
                else:
                    member.settled = 'NO'
                    member.save()

    control_pay.short_description = 'Controlla i pagamenti'

    def get_queryset(self, request):
        qs = super().get_queryset(request).filter(user__is_active = True)
        if not request.user.has_perm('users.add_applicant'):
            return qs.filter(Q(pk=request.user.pk) | Q(parent=request.user.pk))
        else:
            return qs
