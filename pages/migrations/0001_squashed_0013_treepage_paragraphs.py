# Generated by Django 3.1.2 on 2020-10-25 21:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import filebrowser.fields
import uuid


class Migration(migrations.Migration):

    replaces = [('pages', '0001_initial'), ('pages', '0002_treepage_navigation'), ('pages', '0003_treepage_stream_rendered'), ('pages', '0004_auto_20200330_1234'), ('pages', '0005_homepage_body'), ('pages', '0006_auto_20201019_2343'), ('pages', '0007_auto_20201020_1700'), ('pages', '0008_auto_20201020_1802'), ('pages', '0009_auto_20201020_2248'), ('pages', '0010_galleryimage_post'), ('pages', '0011_auto_20201022_0014'), ('pages', '0012_auto_20201022_0022'), ('pages', '0013_treepage_paragraphs')]

    initial = True

    dependencies = [
        ('portfolio', '0008_auto_20201020_1700'),
        ('blog', '0005_auto_20201021_2014'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('intro', models.CharField(blank=True, help_text='Il sito in due parole', max_length=100, null=True, verbose_name='Sottotitolo')),
                ('body', models.TextField(blank=True, help_text='Un testo di presentazione', null=True, verbose_name='Testo')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data:')),
                ('title', models.CharField(blank=True, help_text='Compare sulla prima immagine', max_length=50, null=True, verbose_name='Titolo')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Home Page',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='HomeButton',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True, verbose_name='Titolo')),
                ('subtitle', models.CharField(max_length=200, null=True, verbose_name='Sottotitolo')),
                ('link', models.URLField(null=True, verbose_name='Link')),
                ('position', models.PositiveSmallIntegerField(null=True, verbose_name='Posizione')),
                ('home', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_button', to='pages.homepage')),
            ],
            options={
                'verbose_name': 'Pulsante di Home Page',
                'verbose_name_plural': 'Pulsanti di Home Page',
            },
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_image', filebrowser.fields.FileBrowseField(max_length=200, null=True, verbose_name='Immagine')),
                ('caption', models.CharField(blank=True, max_length=200, null=True, verbose_name='Didascalia')),
                ('position', models.PositiveSmallIntegerField(null=True, verbose_name='Posizione')),
                ('home', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_image', to='pages.homepage')),
                ('image', models.ImageField(editable=False, max_length=200, null=True, upload_to='uploads/images/galleries/', verbose_name='Immagine')),
                ('prog', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_image', to='portfolio.project')),
                ('post', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_image', to='blog.article')),
            ],
            options={
                'verbose_name': 'Immagine',
                'verbose_name_plural': 'Immagini',
            },
        ),
        migrations.CreateModel(
            name='TreePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(max_length=50, verbose_name='Titolo')),
                ('slug', models.SlugField(blank=True, help_text="Titolo come appare nell'indirizzo della pagina,\n            solo lettere minuscole e senza spazi", null=True, unique=True, verbose_name='Slug')),
                ('intro', models.CharField(blank=True, max_length=200, null=True, verbose_name='Introduzione')),
                ('summary', models.BooleanField(default=True, verbose_name='Mostra sommario')),
                ('last_updated', models.DateTimeField(editable=False, null=True)),
                ('navigation', models.BooleanField(default=True, verbose_name='Mostra navigazione')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Testo')),
                ('paragraphs', models.JSONField(editable=False, null=True)),
            ],
            options={
                'verbose_name': 'Pagina ad albero',
                'verbose_name_plural': 'Pagine ad albero',
            },
        ),
    ]
