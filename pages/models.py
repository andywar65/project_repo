from django.contrib.contenttypes.models import ContentType
from django.db import models
from treebeard.mp_tree import MP_Node
from streamfield.fields import StreamField
from streamblocks.models import (IndexedParagraph, CaptionedImage, Gallery,
    LandscapeGallery, DownloadableFile, LinkableList, BoxedText, HomeButton)

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

class TreePage(MP_Node):
    title = models.CharField('Titolo', max_length = 50)

    node_order_by = ['title']

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Pagina ad albero'
        verbose_name_plural = 'Pagine ad albero'

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
        type = ContentType.objects.get(app_label='pages', model='institutional').id
        id = self.id
        stream_list = self.stream.from_json()
        update_indexed_paragraphs(stream_list, type, id)

    class Meta:
        verbose_name = 'Pagina istituzionale'
        verbose_name_plural = 'Pagine istituzionali'
