# Generated by Django 3.1.2 on 2020-10-25 12:45

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('blog', '0008_remove_article_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='Lista di categorie separate da virgole', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Categorie'),
        ),
    ]