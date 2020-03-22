from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.db import models
from treebeard.mp_tree import MP_Node
from project.utils import generate_unique_slug, update_indexed_paragraphs
from streamfield.fields import StreamField
from streamblocks.models import (IndexedParagraph, CaptionedImage, Gallery,
    LandscapeGallery, DownloadableFile, LinkableList, BoxedText, HomeButton)

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
    slug = models.SlugField('Slug', max_length=50, null=True, blank=True,
        unique = True,
        help_text = """Titolo come appare nell'indirizzo della pagina,
            solo lettere minuscole e senza spazi""")
    intro = models.TextField('Introduzione',
        blank= True, null=True, max_length = 200)
    stream = StreamField( model_list=[ IndexedParagraph, CaptionedImage,
        Gallery, DownloadableFile, LinkableList, BoxedText, ],
        verbose_name="Testo" )
    summary = models.BooleanField('Mostra sommario', default = True, )
    last_updated = models.DateTimeField(editable=False, null=True)

    #node_order_by = ['title']

    def get_path(self):
        path = '/docs/'
        ancestors = self.get_ancestors()
        if ancestors:
            for ancestor in ancestors:
                path += ancestor.slug + '/'
        path += self.slug
        return path

    def get_paragraphs(self):
        paragraphs = []
        for block in self.stream.from_json():
            if block['model_name'] == 'IndexedParagraph':
                par = IndexedParagraph.objects.get(id=block['id'])
                paragraphs.append( (par.get_slug, par.title) )
        return paragraphs

    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = self.slug.lower()
        else:
            self.slug = generate_unique_slug(TreePage, self.title)
        self.last_updated = now()
        super(TreePage, self).save(*args, **kwargs)
        #update parent_type end parent_id in IndexedParagraph streamblocks
        #sometimes self.stream returned as string
        if not isinstance(self.stream, str):
            stream_list = self.stream.from_json()
        else:
            from json import loads
            stream_list = loads(self.stream)
        type = ContentType.objects.get(app_label='pages', model='treepage').id
        id = self.id
        update_indexed_paragraphs(stream_list, type, id)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Pagina ad albero'
        verbose_name_plural = 'Pagine ad albero'
