from django.db import models

from blog.models import Article
from pages.models import TreePage

class StreamHelper(models.Model):
    article = models.ForeignKey( Article, on_delete = models.CASCADE,
        null = True, related_name='article_stream_helper' )
    page = models.ForeignKey( TreePage, on_delete = models.CASCADE,
        null = True, related_name='page_stream_helper' )
    stream_type = models.CharField( max_length = 50 )
    stream_id = models.IntegerField()
