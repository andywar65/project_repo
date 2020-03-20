from datetime import datetime
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now
from django.utils.text import slugify
from filebrowser.fields import FileBrowseField
from taggit.managers import TaggableManager
from streamfield.fields import StreamField
from streamblocks.models import (IndexedParagraph, CaptionedImage, Gallery,
    LandscapeGallery, DownloadableFile, LinkableList, BoxedText, HomeButton)
from users.models import User

def generate_unique_slug(klass, field):
    """
    return unique slug if origin slug exists.
    eg: `foo-bar` => `foo-bar-1`

    :param `klass` is Class model.
    :param `field` is specific field for title.
    Thanks to djangosnippets.org!
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug

def update_indexed_paragraphs(stream_list, type, id):
    for block in stream_list:
        if block['model_name'] == 'IndexedParagraph':
            par = IndexedParagraph.objects.get(id = block['id'])
            par.parent_type = type
            par.parent_id = id
            par.save()

class HomePage(models.Model):

    carousel = StreamField(model_list=[ LandscapeGallery, ],
        null=True, blank=True, verbose_name="Galleria orizzontale",
        help_text="Una sola galleria, per favore, larghezza minima immagini 2048px")
    intro = models.CharField('Sottotitolo', max_length = 100,
        null=True, blank=True, help_text = 'Il sito in due parole')
    action = StreamField(model_list=[ HomeButton, ],
        null=True, blank=True, verbose_name="Pulsanti di azione",
        help_text="Link a pagine sponsorizzate.")

    class Meta:
        verbose_name = 'Home Page'

class Institutional(models.Model):
    title = models.CharField('Titolo', max_length = 50)
    slug = models.SlugField('Slug', max_length=50, null=True, unique = True,
        help_text = """Titolo come appare nell'indirizzo della pagina,
            solo lettere minuscole e senza spazi""")
    intro = models.TextField('Introduzione',
        blank= True, null=True, max_length = 200)
    stream = StreamField( model_list=[ IndexedParagraph, CaptionedImage,
        Gallery, DownloadableFile, LinkableList, BoxedText, ],
        verbose_name="Testo" )
    summary = models.BooleanField('Mostra sommario', default = True, )

    def get_paragraphs(self):
        paragraphs = []
        for block in self.stream.from_json():
            if block['model_name'] == 'IndexedParagraph':
                par = IndexedParagraph.objects.get(id=block['id'])
                paragraphs.append( (par.get_slug, par.title) )
        return paragraphs

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self.slug.lower()
        super(Institutional, self).save(*args, **kwargs)
        #update parent_type end parent_id in IndexedParagraph streamblocks
        type = ContentType.objects.get(app_label='pagine', model='institutional').id
        id = self.id
        stream_list = self.stream.from_json()
        update_indexed_paragraphs(stream_list, type, id)

    class Meta:
        verbose_name = 'Pagina istituzionale'
        verbose_name_plural = 'Pagine istituzionali'
