# Generated by Django 3.1.2 on 2020-11-06 18:22

from django.db import migrations, models
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='galleryimage',
            options={'verbose_name': 'Immagine', 'verbose_name_plural': 'Images'},
        ),
        migrations.AlterModelOptions(
            name='homebutton',
            options={'verbose_name': 'Home Page button', 'verbose_name_plural': 'Home Page buttons'},
        ),
        migrations.AlterModelOptions(
            name='treepage',
            options={'verbose_name': 'Tree page', 'verbose_name_plural': 'Tree pages'},
        ),
        migrations.AlterField(
            model_name='galleryimage',
            name='caption',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Caption'),
        ),
        migrations.AlterField(
            model_name='galleryimage',
            name='fb_image',
            field=filebrowser.fields.FileBrowseField(max_length=200, null=True, verbose_name='Images'),
        ),
        migrations.AlterField(
            model_name='galleryimage',
            name='image',
            field=models.ImageField(editable=False, max_length=200, null=True, upload_to='uploads/images/galleries/', verbose_name='Images'),
        ),
        migrations.AlterField(
            model_name='galleryimage',
            name='position',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Position'),
        ),
        migrations.AlterField(
            model_name='homebutton',
            name='position',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Position'),
        ),
        migrations.AlterField(
            model_name='homebutton',
            name='subtitle',
            field=models.CharField(max_length=200, null=True, verbose_name='Subtitle'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=models.TextField(blank=True, help_text='Talk about this website', null=True, verbose_name='Testo'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='intro',
            field=models.CharField(blank=True, help_text='Website in few words', max_length=100, null=True, verbose_name='Subtitle'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='title',
            field=models.CharField(blank=True, help_text='Appears on first image', max_length=50, null=True, verbose_name='Titolo'),
        ),
        migrations.AlterField(
            model_name='treepage',
            name='navigation',
            field=models.BooleanField(default=True, verbose_name='Show navigation'),
        ),
        migrations.AlterField(
            model_name='treepage',
            name='slug',
            field=models.SlugField(blank=True, help_text='Title as it appears in the address bar,\n            only lowercas, no blank spaces', null=True, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='treepage',
            name='summary',
            field=models.BooleanField(default=True, verbose_name='Show summary'),
        ),
    ]
