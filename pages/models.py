import uuid

from django.utils.timezone import now
from django.utils.html import strip_tags
from django.db import models

from filebrowser.fields import FileBrowseField
from treebeard.mp_tree import MP_Node

from project.utils import generate_unique_slug
from streamfield.base import StreamObject
from streamfield.fields import StreamField
from streamblocks.models import (IndexedParagraph, CaptionedImage, Gallery,
    LandscapeGallery, DownloadableFile, LinkableList, BoxedText, HomeButton)

class HomePage(models.Model):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Titolo',
        help_text="Compare sulla prima immagine",
        max_length = 50, null=True, blank=True)
    intro = models.CharField('Sottotitolo', max_length = 100,
        null=True, blank=True, help_text = 'Il sito in due parole')
    body = models.TextField('Testo',
        null=True, blank=True, help_text = 'Un testo di presentazione')
    date = models.DateTimeField('Data:', default = now, )

    def __str__(self):
        return self.title if self.title else str(self.uuid)

    class Meta:
        verbose_name = 'Home Page'
        ordering = ('-date', )

class GalleryImage(models.Model):
    home = models.ForeignKey(HomePage, null=True, editable=False,
        on_delete = models.CASCADE, related_name='home_image')
    fb_image = FileBrowseField("Immagine", max_length=200,
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        null=True)
    caption = models.CharField("Didascalia", max_length = 200, blank=True,
        null=True)
    position = models.PositiveSmallIntegerField("Posizione", null=True)

    class Meta:
        verbose_name="Immagine"
        verbose_name_plural="Immagini"

class HomeButton(models.Model):
    home = models.ForeignKey(HomePage, null=True, editable=False,
        on_delete = models.CASCADE, related_name='home_button')
    title = models.CharField("Titolo", max_length = 100, null=True )
    subtitle = models.CharField("Sottotitolo", max_length = 200, null=True )
    link = models.URLField("Link", max_length = 200, null=True, )
    position = models.PositiveSmallIntegerField("Posizione", null=True)

    class Meta:
        verbose_name="Pulsante di Home Page"
        verbose_name_plural="Pulsanti di Home Page"

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
    stream_search = models.TextField(editable=False, null=True)
    summary = models.BooleanField('Mostra sommario', default = True, )
    navigation = models.BooleanField('Mostra navigazione', default = True, )
    last_updated = models.DateTimeField(editable=False, null=True)

    #node_order_by = ['title']

    def get_path(self):
        path = '/docs/'
        ancestors = self.get_ancestors()
        if ancestors:
            for ancestor in ancestors:
                path += ancestor.slug + '/'
        path += self.slug + '/'
        return path

    def get_paragraphs(self):
        paragraphs = []
        for block in self.stream.from_json():
            if block['model_name'] == 'IndexedParagraph':
                par = IndexedParagraph.objects.get(id=block['id'])
                paragraphs.append( (par.get_slug(), par.title) )
        return paragraphs

    def get_adjacent_pages(self):
        root = self.get_root()
        annotated_list = TreePage.get_annotated_list( parent = root )
        page_list = []
        for item in annotated_list:
            page_list.append(item[0])
        length = len(page_list)
        next = None
        prev = None
        if length == 1:
            return prev, next
        i = 0
        for page in page_list:
            if page == self:
                if i>0:
                    prev = page_list[i-1]
                if i<(length-1):
                    next = page_list[i+1]
            i += 1
        return prev, next

    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = self.slug.lower()
        else:
            self.slug = generate_unique_slug(TreePage, self.title)
        self.last_updated = now()
        #sometimes treats stream as str instead of StreamField object
        #probably should use transaction instaed
        #but for now this patch works
        if isinstance(self.stream, str):
            tmp = StreamObject( value = self.stream,
                model_list=[ IndexedParagraph, CaptionedImage,
                    Gallery, DownloadableFile, LinkableList, BoxedText, ], )
            self.stream_search = strip_tags(tmp.render)
        else:
            self.stream_search = strip_tags(self.stream.render)
        super(TreePage, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Pagina ad albero'
        verbose_name_plural = 'Pagine ad albero'
