import os
from PIL import Image
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMessage
from .choices import *

def user_directory_path(instance, filename):
    return 'uploads/users/{0}/{1}'.format(instance.user.username, filename)

class User(AbstractUser):

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.is_active:
            try:
                memb = Profile.objects.get(user_id = self.id)
                return
            except:
                memb = Profile.objects.create(user = self)
                memb.save()
                return

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,
        primary_key=True, editable=False)
    sector = models.CharField(max_length = 4, choices = SECTOR,
        default = '0-NO', verbose_name = 'Corre con noi?')
    parent = models.ForeignKey(User, on_delete = models.SET_NULL,
        blank = True, null = True, related_name = 'member_parent',
        verbose_name = 'Genitore')
    first_name = models.CharField('Nome', default = 'Nome',
        max_length = 50,)
    last_name = models.CharField('Cognome', default = 'Cognome',
        max_length = 50,)
    email = models.EmailField('Email', default = 'me@example.com',
        )
    avatar = models.ImageField(blank = True, null=True,
        upload_to = user_directory_path,)
    thumb = models.CharField(editable=False, blank=True, null=True,
        max_length = 200,)
    gender = models.CharField(max_length = 1, choices = GENDER,
        blank = True, null=True, verbose_name = 'Sesso', )
    date_of_birth = models.DateField( blank=True, null=True,
        verbose_name = 'Data di nascita',)
    place_of_birth = models.CharField(max_length = 50,
        blank = True, null = True, verbose_name = 'Luogo di nascita',)
    nationality = models.CharField(max_length = 50,
        blank = True, null = True, verbose_name = 'Nazionalità',)
    fiscal_code = models.CharField(max_length = 16,
        blank = True, null = True, verbose_name = 'Codice fiscale',)
    address = models.CharField(max_length = 100,
        blank = True, null = True, verbose_name = 'Indirizzo',
        help_text = 'Via/Piazza, civico, CAP, Città',)
    phone = models.CharField(max_length = 50,
        blank = True, null = True, verbose_name = 'Telefono/i',)
    email_2 = models.EmailField(blank = True, null = True,
        verbose_name = 'Seconda email',)
    no_spam = models.BooleanField(default = True,
        verbose_name = 'Mailing list',
        help_text = 'Vuoi ricevere notifiche sugli eventi?',)
    course = models.ManyToManyField(CourseSchedule,
        blank = True, verbose_name = 'Orari scelti', )
    course_alt = models.CharField(max_length = 100,
        blank = True, null = True, verbose_name = 'Altro orario',)
    course_membership = models.CharField(max_length = 4, choices = COURSE,
        blank = True, null = True, verbose_name = 'Federazione / Ente sportivo',
        help_text = 'Solo se si segue un corso')
    no_course_membership = models.CharField(max_length = 4, choices = NO_COURSE,
        blank = True, null = True, verbose_name = 'Federazione / Ente sportivo',
        help_text = 'Solo se non si segue un corso')
    sign_up = models.FileField(
        upload_to = user_directory_path,
        blank = True, null = True, verbose_name = 'Richiesta di tesseramento',
        )
    privacy = models.FileField(
        upload_to = user_directory_path,
        blank = True, null = True, verbose_name = 'Privacy',
        )
    med_cert = models.FileField(
        upload_to = user_directory_path,
        blank = True, null = True, verbose_name = 'Certificato medico',
        )
    membership = models.CharField(max_length = 50,
        blank = True, null = True, verbose_name = 'Tessera',)
    mc_expiry = models.DateField( blank=True, null=True,
        verbose_name = 'Scadenza CM/CMA',)
    mc_state = models.CharField(max_length = 4, choices = MC_STATE,
        verbose_name = 'Stato del CM/CMA',
        blank = True, null = True, )
    total_amount = models.FloatField( default = 0.00,
        verbose_name = 'Importo totale')
    settled = models.CharField(max_length = 4, choices = SETTLED,
        blank=True, null=True,
        verbose_name = 'In regola?',)

    def get_full_name(self):
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()
    get_full_name.short_description = 'Nome'

    def get_full_name_reverse(self):
        full_name_reverse = '%s %s' % (self.first_name, self.last_name)
        return full_name_reverse.strip()

    def get_thumb(self):
        if self.thumb:
            thumb = format_html('<img src="{}" alt="" class="rounded-circle" />',
                self.thumb)
        else:
            thumb = format_html('<img src="/static/images/thumb_rp.png" alt="" class="rounded-circle" />')
        return thumb
    get_thumb.short_description = ''

    def __str__(self):
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        if self.avatar:
            url_extension = os.path.splitext(self.avatar.url)
            thumb_name = url_extension[0] + "_thumb" + url_extension[1]
            if not self.thumb == thumb_name:
                try:
                    root_extension = os.path.splitext(self.avatar.path)
                    img = Image.open(root_extension[0] + root_extension[1])
                    xsize, ysize = img.size
                    if xsize > ysize:
                        cropped = img.crop(((xsize-ysize)/2,0,
                            xsize-(xsize-ysize)/2,ysize))
                    elif xsize < ysize:
                        cropped = img.crop((0,(ysize-xsize)/2,
                            xsize,ysize-(ysize-xsize)/2))
                    else:
                        cropped = img.copy()
                    size = (32, 32)
                    cropped.thumbnail(size)
                    cropped.save(root_extension[0] + "_thumb" + root_extension[1])
                    self.thumb = thumb_name
                    super(Profile, self).save(*args, **kwargs)
                except:
                    pass

    class Meta:
        verbose_name = 'Iscritto'
        verbose_name_plural = 'Iscritti'

class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='user_message', blank=True, null=True,
        verbose_name = 'Utente', )
    nickname = models.CharField(max_length = 50,
        verbose_name = 'Nome', blank=True, null=True,)
    email = models.EmailField(blank=True, null=True,
        verbose_name = 'Inviato da',)
    recipient = models.EmailField(blank=True, null=True, verbose_name = 'Destinatario')
    subject = models.CharField(max_length = 200,
        verbose_name = 'Soggetto', )
    body = models.TextField(verbose_name = 'Messaggio', )
    attachment = models.FileField(
        upload_to = user_directory_path,
        blank = True, null = True, verbose_name = 'Allegato',
        )
    notice = models.CharField(max_length = 4, choices = NOTICE,
        default = 'SPAM', verbose_name = 'Notifica via email')
    privacy = models.BooleanField( default=False )

    def get_full_name(self):
        if self.user:
            return self.user.member.get_full_name()
        else:
            return self.nickname
    get_full_name.short_description = 'Nome'

    def get_email(self):
        if self.user:
            return self.user.member.email
        else:
            return self.email
    get_email.short_description = 'Indirizzo email'

    def save(self, *args, **kwargs):
        go_spam = False
        if not self.recipient:
            self.recipient = settings.DEFAULT_RECIPIENT
        if self.notice == 'SPAM':
            go_spam = True
            self.notice = 'DONE'
        super(UserMessage, self).save(*args, **kwargs)
        if go_spam:
            subject = self.subject
            message = (self.body + '\n\nDa: '+ self.get_full_name() +
                ' (' + self.get_email() + ')')
            mailto = [self.recipient, ]
            email = EmailMessage(subject, message, settings.SERVER_EMAIL,
                mailto)
            if self.attachment:
                email.attach_file(self.attachment.path)
            email.send()

    def __str__(self):
        return 'Messaggio - %s' % (self.id)

    class Meta:
        verbose_name = 'Messaggio'
        verbose_name_plural = 'Messaggi'
