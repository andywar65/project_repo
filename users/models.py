import os
import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _

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
    get_full_name.short_description = _('Name')

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        else:
            return self.username

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.is_active:
            memb, created = Profile.objects.get_or_create(user_id = self.uuid)

    class Meta:
        ordering = ('last_name', 'first_name', 'username')

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,
        primary_key=True, editable=False )
    avatar = models.ImageField(blank = True, null=True,
        upload_to = 'uploads/users/')
    bio = models.TextField(_("Short bio"), null=True, blank=True)
    yes_spam = models.BooleanField(default = False,
        verbose_name = _('Mailing list'),
        help_text = _("Do you want to be notified on new articles?"),)
    immutable = models.BooleanField(default = False,)

    def get_full_name(self):
        return self.user.get_full_name()
    get_full_name.short_description = _('Name')

    def get_thumb(self):
        if self.avatar:
            return FileObject(str(self.avatar))
        return

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

def user_private_directory_path(instance, filename):
    root = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]
    filename = '%s_%s%s' % (root, get_random_string(7), ext)
    return 'users/{0}/{1}'.format(instance.user.username, filename)

class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='user_message', blank=True, null=True,
        verbose_name = _('User'), )
    nickname = models.CharField(max_length = 50,
        verbose_name = _('Name'), blank=True, null=True,)
    email = models.EmailField(blank=True, null=True,
        verbose_name = _('From'),)
    recipient = models.EmailField(blank=True, null=True,
        verbose_name = _('To'))
    subject = models.CharField(max_length = 200,
        verbose_name = _('Subject'), )
    body = models.TextField(verbose_name = _('Text'), )
    attachment = PrivateFileField(
        upload_to = user_private_directory_path,
        blank = True, null = True, verbose_name = _('Attachment'),
        )
    privacy = models.BooleanField( _('Privacy'), default=False )

    def get_full_name(self):
        if self.user:
            return self.user.get_full_name()
        else:
            return self.nickname
    get_full_name.short_description = _('Name')

    def get_email(self):
        if self.user:
            return self.user.email
        else:
            return self.email
    get_email.short_description = _('Email address')

    def __str__(self):
        return _('Message - %(id)d') % {'id': self.id}

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
