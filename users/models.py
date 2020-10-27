import os
import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from django.contrib.auth.models import Group

from PIL import Image
from private_storage.fields import PrivateFileField
from filebrowser.fields import FileBrowseField
from filebrowser.base import FileObject

class User(AbstractUser):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return self.username
    get_full_name.short_description = 'Nome'

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        else:
            return self.username

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.is_active:
            memb, created = Profile.objects.get_or_create(user_id = self.id)

    class Meta:
        ordering = ('last_name', 'first_name', 'username')

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,
        primary_key=True, editable=False )
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

def user_private_directory_path(instance, filename):
    root = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]
    filename = '%s_%s%s' % (root, get_random_string(7), ext)
    return 'users/{0}/{1}'.format(instance.user.username, filename)

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
    attachment = PrivateFileField(
        upload_to = user_private_directory_path,
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
