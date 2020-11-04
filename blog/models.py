import uuid
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext as _

from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

from project.utils import generate_unique_slug
from users.models import User
from .choices import *

class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

def default_intro():
    return _('Another article by %(name)s!') % {'name': settings.WEBSITE_NAME}

class Article(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, editable=False, null=True)
    title = models.CharField(_('Title'),
        help_text=_("The title of the article"),
        max_length = 50)
    intro = models.CharField(_('Introduction'),
        default = default_intro,
        max_length = 100)
    body = models.TextField(_('Text'), null=True)
    date = models.DateField(_('Date'), default = now, )
    last_updated = models.DateTimeField(editable=False, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
        blank= True, null=True, verbose_name = _('Author'))
    tags = TaggableManager(verbose_name=_("Categories"),
        help_text=_("Comma separated list of categories"),
        through=UUIDTaggedItem, blank=True)
    notice = models.CharField(max_length = 4, choices = NOTICE,
        blank = True, null = True, verbose_name = _('Notify by email'),
        help_text = _("""Send automatic notification by selecting
            'Send notification' and saving the article.
            """))

    def get_path(self):
        temp = self.date
        #conditional added for test to work
        if isinstance(temp, str):
            temp = temp.split(' ')[0]
            temp = datetime.strptime(temp, '%Y-%m-%d')
        return _('/articles/') + temp.strftime("%Y/%m/%d") + '/' + self.slug

    def get_uploads(self):
        return self.article_uploads.all()

    def get_tags(self):
        return list(self.tags.names())

    def get_previous(self):
        try:
            return self.get_previous_by_date()
        except Article.DoesNotExist:
            return

    def get_next(self):
        try:
            return self.get_next_by_date()
        except Article.DoesNotExist:
            return

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Article, self.title)
        self.last_updated = now()
        if self.notice == 'SPAM':
            message = self.title + '\n'
            message += self.intro + '\n'
            url = settings.BASE_URL + self.get_path()
            message += _('Follow this link to read it: ') + url + '\n'
            recipients = User.objects.filter( is_active = True, )
            #inactive users may not have profile
            recipients = recipients.filter( profile__yes_spam = True, )
            mailto = []
            for recipient in recipients:
                mailto.append(recipient.email)
            subject = _('New article on %(name)s ') % {'name': settings.WEBSITE_NAME}
            email = EmailMessage(subject, message, settings.SERVER_EMAIL,
                mailto)
            email.send()
            self.notice = 'DONE'
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ('-date', )

class UserUpload(models.Model):
    post = models.ForeignKey(Article, on_delete = models.CASCADE,
        null = True, related_name='article_uploads')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True,
        verbose_name = _('User'))
    date = models.DateTimeField(_('Date'), default = now, )
    image = models.ImageField(_('Image'), blank = True, null = True,
        upload_to = 'uploads/articles/users/',)
    body = models.CharField(_('Text'), help_text = _("Write something."),
        max_length=500 )

    def __str__(self):
        return _('Contribution - ') + str(self.id)

    class Meta:
        verbose_name = _('Contribution')
        verbose_name_plural = _('Contributions')
        ordering = ('-id', )
