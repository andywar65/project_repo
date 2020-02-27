# Generated by Django 3.0.2 on 2020-02-06 18:32

from django.db import migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pagine', '0003_auto_20200204_0847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='image',
        ),
        migrations.AddField(
            model_name='blog',
            name='fb_image',
            field=filebrowser.fields.FileBrowseField(blank=True, max_length=200, null=True, verbose_name='Immagine'),
        ),
    ]
