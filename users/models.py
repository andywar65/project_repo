import os
from PIL import Image
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMessage
from .choices import *

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
    avatar =FileBrowseField("Immagine", max_length=200,
        directory="users/",
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        null=True, blank=True)
    no_spam = models.BooleanField(default = True,
        verbose_name = 'Mailing list',
        help_text = 'Vuoi ricevere notifiche sugli eventi?',)

    def get_full_name(self):
        return self.user.get_full_name()
    get_full_name.short_description = 'Nome'

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Profilo'
        verbose_name_plural = 'Profili'

class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='user_message', blank=True, null=True,
        verbose_name = 'Utente', )
    nickname = models.CharField(max_length = 50,
        verbose_name = 'Nome', blank=True, null=True,)
    email = models.EmailField(blank=True, null=True,
        verbose_name = 'Inviato da',)
    recipient = models.EmailField(blank=True, null=True,
        verbose_name = 'Destinatario')
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
            return self.user.get_full_name()
        else:
            return self.nickname
    get_full_name.short_description = 'Nome'

    def get_email(self):
        if self.user:
            return self.user.email
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
