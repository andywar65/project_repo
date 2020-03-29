from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now
from taggit.managers import TaggableManager
from project.utils import generate_unique_slug, update_indexed_paragraphs
from streamfield.fields import StreamField
from helper.models import StreamHelper, update_streamblocks
from streamblocks.models import (IndexedParagraph, CaptionedImage, Gallery,
    LandscapeGallery, DownloadableFile, LinkableList, BoxedText, HomeButton)
from users.models import User
from .choices import *

class Article(models.Model):
    carousel = StreamField(model_list=[ LandscapeGallery, ],
        null=True, blank=True, verbose_name="Galleria",
        help_text="Una sola galleria, per favore, larghezza minima immagini 2048px")
    title = models.CharField('Titolo',
        help_text="Il titolo dell'articolo",
        max_length = 50)
    slug = models.SlugField(max_length=50, editable=False, null=True)
    date = models.DateTimeField('Data', default = now, )
    last_updated = models.DateTimeField(editable=False, null=True)
    intro = models.CharField('Introduzione',
        default = 'Un altro articolo di approfondimento!', max_length = 100)
    stream = StreamField( model_list=[ IndexedParagraph, CaptionedImage,
            Gallery, DownloadableFile, LinkableList, BoxedText],
            verbose_name="Testo" )
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
        blank= True, null=True, verbose_name = 'Autore')
    tags = TaggableManager(verbose_name="Categorie",
        help_text="Lista di categorie separate da virgole",
        through=None, blank=True)
    notice = models.CharField(max_length = 4, choices = NOTICE,
        blank = True, null = True, verbose_name = 'Notifica via email',
        help_text = """Invia notifica in automatico selezionando
            'Invia notifica' e salvando l'articolo.
            """)

    def get_image(self):
        gallery_list = self.carousel.from_json()
        if gallery_list:
            gallery = gallery_list[0]
            image = LandscapeGallery.objects.filter( id__in = gallery['id'] ).first()
            return image.fb_image
        return

    def get_path(self):
        return '/articoli/' + self.date.strftime("%Y/%m/%d") + '/' + self.slug

    def get_uploads(self):
        return UserUpload.objects.filter(post_id=self.id)

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
            message += 'Fai click su questo link per leggerlo: ' + url + '\n'
            recipients = User.objects.filter( is_active = True, )
            #inactive users may not have profile
            recipients = recipients.filter( profile__no_spam = True, )
            mailto = []
            for recipient in recipients:
                mailto.append(recipient.email)
            subject = f'Nuovo articolo su {settings.WEBSITE_NAME}'
            email = EmailMessage(subject, message, settings.SERVER_EMAIL,
                mailto)
            email.send()
            self.notice = 'DONE'
        super(Article, self).save(*args, **kwargs)
        #update parent_type end parent_id in streamblock helpers
        type = ContentType.objects.get(app_label='blog', model='article').id
        id = self.id
        stream_list = self.stream.from_json()
        stream_list += self.carousel.from_json()
        update_streamblocks(stream_list, type, id)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Articolo'
        verbose_name_plural = 'Articoli'
        ordering = ('-date', )

class UserUpload(models.Model):
    post = models.ForeignKey(Article, on_delete = models.CASCADE,
        null = True, related_name='article_uploads')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True,
        verbose_name = 'Utente')
    date = models.DateTimeField('Data', default = now, )
    image = models.ImageField('Immagine', blank = True, null = True,
        upload_to = 'uploads/articles/users/',)
    body = models.TextField('Testo', help_text = "Scrivi qualcosa.", )

    def __str__(self):
        return 'Contributo - ' + str(self.id)

    class Meta:
        verbose_name = 'Contributo'
        verbose_name_plural = 'Contributi'
        ordering = ('-id', )
