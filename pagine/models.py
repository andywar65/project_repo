from PIL import Image
from datetime import datetime
from django.db import models
from django.utils.timezone import now
from django.utils.text import slugify
from filebrowser.fields import FileBrowseField
from taggit.managers import TaggableManager
from streamfield.fields import StreamField
from streamblocks.models import (IndexedParagraph, CaptionedImage,
    DownloadableFile, LinkableList, BoxedText, )
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

class Blog(models.Model):
    fb_image = FileBrowseField("Immagine", max_length=200, directory="blogs/",
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        null=True, blank=True)
    carousel = StreamField(model_list=[ LandscapeGallery, ],
        null=True, blank=True, verbose_name="Galleria",
        help_text="Una sola galleria, per favore, larghezza minima immagini 2048px")
    title = models.CharField('Titolo',
        help_text="Il titolo dell'articolo",
        max_length = 50)
    slug = models.SlugField(max_length=50, editable=False, null=True)
    date = models.DateTimeField('Data', default = now())
    last_updated = models.DateTimeField(editable=False, null=True)
    intro = models.CharField('Introduzione',
        default = 'Un altro articolo di approfondimento da RP!', max_length = 100)
    stream = StreamField( model_list=[ IndexedParagraph, CaptionedImage,
            DownloadableFile, LinkableList, BoxedText], verbose_name="Testo" )
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
        blank= True, null=True, verbose_name = 'Autore')
    tags = TaggableManager(verbose_name="Categorie",
        help_text="Lista di categorie separate da virgole",
        through=None, blank=True)

    def get_path(self):
        return '/articoli/' + self.slug

    def get_uploads(self):
        return UserUpload.objects.filter(post_id=self.id)

    def get_tags(self):
        return list(self.tags.names())

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Blog, self.title)
        self.last_updated = now()
        super(Blog, self).save(*args, **kwargs)
        #update parent_type end parent_id in IndexedParagraph streamblocks
        type = ContentType.objects.get(app_label='pagine', model='blog').id
        id = self.id
        stream_list = self.stream.from_json()
        update_indexed_paragraphs(stream_list, type, id)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Articolo'
        verbose_name_plural = 'Articoli'
        ordering = ('-date', )

class UserUpload(models.Model):
    post = models.ForeignKey(Blog, on_delete = models.CASCADE,
        null = True, related_name='blog_uploads')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True,
        verbose_name = 'Utente')
    date = models.DateTimeField('Data', default = now, )
    image = models.ImageField('Immagine', blank = True, null = True,
        upload_to = 'uploads/blogs/users/',)
    body = models.TextField('Testo', help_text = "Scrivi qualcosa.", )

    def __str__(self):
        return 'Contributo - ' + str(self.id)

    class Meta:
        verbose_name = 'Contributo'
        verbose_name_plural = 'Contributi'
        ordering = ('-id', )
