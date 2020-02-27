import os
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from filebrowser.fields import FileBrowseField
from .choices import *

class IndexedParagraph(models.Model):
    height = models.CharField('Altezza titolo', max_length=1, choices = HEIGHT,
        default='4')
    title = models.CharField('Titolo', max_length = 100, blank=True, null=True)
    body = models.TextField('Testo', blank=True, null=True,
        help_text="Accetta tag HTML")

    def get_slug(self):
        return slugify( self.title )

    class Meta:
        verbose_name="Paragrafo indicizzato"
        verbose_name_plural="Paragrafi indicizzati"

class CaptionedImage(models.Model):
    fb_image = FileBrowseField("Immagine", max_length=200,
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        null=True)
    caption = models.CharField("Didascalia", max_length = 200, blank=True,
        null=True)

    class Meta:
        verbose_name="Immagine con didascalia"
        verbose_name_plural="Immagini con didascalia"

class DownloadableFile(models.Model):
    fb_file = FileBrowseField("File", max_length=200, directory="documents/",
        extensions=[".pdf", ".doc", ".rtf", ".txt", ".xls", ".csv", ".docx"],
        null=True )
    description = models.CharField("Descrizione", max_length = 200, blank=True,
        null=True )

    def get_description(self):
        if self.description:
            return self.description
        return self.fb_file.filename

    class Meta:
        verbose_name="File scaricabile"
        verbose_name_plural="File scaricabili"

class LinkableList(models.Model):
    text = models.CharField("Elemento", max_length = 200, null=True )
    link = models.URLField("Link", max_length = 200, null=True, blank=True )

    as_list = True

    options = {
        'ol_ul': {
            'label': 'Tipo',
            'type': 'select',
            'default': 'ul',
            'options': [
                {'value': 'ul', 'name': 'Lista non ordinata'},
                {'value': 'ol', 'name': 'Lista ordinata'},
            ]
        }
    }

    class Meta:
        verbose_name="Lista con link"
        verbose_name_plural="Liste con link"

class BoxedText(models.Model):
    color = models.CharField('Colore', max_length=10, choices = COLOR,
        default='success')
    body = models.TextField('Testo', null=True,)

    class Meta:
        verbose_name="Testo in un box"
        verbose_name_plural="Testi in un box"

class EventUpgrade(models.Model):
    title = models.CharField('Titolo',
        help_text="Il titolo dell'aggiornamento",
        max_length = 50)
    date = models.DateTimeField('Data', default = now)
    body = models.TextField('Aggiornamento',
        help_text = "Accetta tag HTML.", )

    class Meta:
        verbose_name = 'Aggiornamento'
        verbose_name_plural = 'Aggiornamenti'

# Register blocks for StreamField as list of models
STREAMBLOCKS_MODELS = [
    IndexedParagraph,
    CaptionedImage,
    DownloadableFile,
    LinkableList,
    BoxedText,
    EventUpgrade,
]
