import os
from PIL import Image
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMessage
from filebrowser.fields import FileBrowseField
from filebrowser.base import FileObject

class User(AbstractUser):

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return self.username

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        else:
            return self.username

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
    avatar = models.ImageField(blank = True, null=True,
        upload_to = 'uploads/users/')
    bio = models.TextField("Breve biografia", null=True, blank=True)
    yes_spam = models.BooleanField(default = False,
        verbose_name = 'Mailing list',
        help_text = 'Vuoi ricevere notifiche sugli eventi?',)

    def get_full_name(self):
        return self.user.get_full_name()
    get_full_name.short_description = 'Nome'

    def get_thumb(self):
        if self.avatar:
            return FileObject(str(self.avatar))
        return

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
        upload_to = 'uploads/users/',
        blank = True, null = True, verbose_name = 'Allegato',
        )
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

    def __str__(self):
        return 'Messaggio - %s' % (self.id)

    class Meta:
        verbose_name = 'Messaggio'
        verbose_name_plural = 'Messaggi'
