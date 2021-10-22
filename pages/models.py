import uuid
import json

from django.utils.timezone import now
from django.utils.html import strip_tags
from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse

from filebrowser.fields import FileBrowseField
from treebeard.mp_tree import MP_Node

from project.utils import generate_unique_slug
from blog.models import Article
from portfolio.models import Project

class HomePage(models.Model):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Title'),
        help_text=_("Appears on first image"),
        max_length = 50, null=True, blank=True)
    intro = models.CharField(_('Subtitle'), max_length = 100,
        null=True, blank=True, help_text = _('Website in few words'))
    body = models.TextField(_('Text'),
        null=True, blank=True, help_text = _('Talk about this website'))
    date = models.DateTimeField(_('Date:'), default = now, )

    def __str__(self):
        return self.title if self.title else str(self.uuid)

    class Meta:
        verbose_name = _('Home Page')
        ordering = ('-date', )

class GalleryImage(models.Model):
    home = models.ForeignKey(HomePage, null=True, editable=False,
        on_delete = models.CASCADE, related_name='home_image')
    prog = models.ForeignKey(Project, null=True, editable=False,
        on_delete = models.CASCADE, related_name='project_image')
    post = models.ForeignKey(Article, null=True, editable=False,
        on_delete = models.CASCADE, related_name='article_image')
    image = models.ImageField(_("Images"), max_length=200, editable = False,
        null=True, upload_to='uploads/images/galleries/')
    fb_image = FileBrowseField(_("Images"), max_length=200,
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        null=True, directory='images/galleries/')
    caption = models.CharField(_("Caption"), max_length = 200, blank=True,
        null=True)
    position = models.PositiveSmallIntegerField(_("Position"), null=True)

    class Meta:
        verbose_name=_("Image")
        verbose_name_plural=_("Images")
        ordering = ( 'position', )

class HomeButton(models.Model):
    home = models.ForeignKey(HomePage, null=True, editable=False,
        on_delete = models.CASCADE, related_name='home_button')
    title = models.CharField(_('Title'), max_length = 100, null=True )
    subtitle = models.CharField(_('Subtitle'), max_length = 200, null=True )
    link = models.URLField(_('Link'), max_length = 200, null=True, )
    position = models.PositiveSmallIntegerField(_("Position"), null=True)

    class Meta:
        verbose_name=_("Home Page button")
        verbose_name_plural=_("Home Page buttons")
        ordering = ( 'position', )

class TreePage(MP_Node):
    title = models.CharField(_('Title'), max_length = 50)
    slug = models.SlugField(_('Slug'), max_length=50, null=True, blank=True,
        unique = True,
        help_text = _("""Title as it appears in the address bar,
            only lowercase, no blank spaces"""))
    intro = models.CharField(_('Introduction'),
        blank= True, null=True, max_length = 200)
    body = models.TextField(_('Text'), null=True, blank=True,)
    summary = models.BooleanField(_('Show summary'), default = True, )
    navigation = models.BooleanField(_('Show navigation'), default = True, )
    last_updated = models.DateTimeField(editable=False, null=True)
    paragraphs = models.JSONField(editable=False, null=True, )

    #node_order_by = ['title']

    def get_path(self):
        path = reverse('docs:page_list')
        ancestors = self.get_ancestors()
        if ancestors:
            for ancestor in ancestors:
                path += ancestor.slug + '/'
        path += self.slug + '/'
        return path

    def get_paragraphs(self):
        #serve paragraphs without touching body
        txt = self.body
        for num, title in self.paragraphs.items():
            txt = txt.replace('class="indexed_paragraph"',
                f'id="paragraph-{num}"', 1)
        return txt

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
        #prepare paragraphs without touching body
        self.paragraphs = {}
        txt = self.body
        count = txt.count('class="indexed_paragraph">')
        for c in range(count):
            txt = txt.split('class="indexed_paragraph">', 1)[1]
            self.paragraphs[c] = txt.split('</h4>', 1)[0]
            txt = txt.split('</h4>', 1)[1]
        super(TreePage, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Tree page')
        verbose_name_plural = _('Tree pages')
