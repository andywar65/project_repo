# Generated by Django 3.1.2 on 2020-10-28 22:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(editable=False, null=True)),
                ('title', models.CharField(help_text="Il titolo dell'articolo", max_length=50, verbose_name='Titolo')),
                ('intro', models.CharField(default='Un altro articolo di approfondimento da architettura.APP!', max_length=100, verbose_name='Introduzione')),
                ('body', models.TextField(null=True, verbose_name='Testo')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Data')),
                ('last_updated', models.DateTimeField(editable=False, null=True)),
                ('notice', models.CharField(blank=True, choices=[('NOSP', 'Non inviare'), ('SPAM', 'Da inviare'), ('DONE', 'Già inviata')], help_text="Invia notifica in automatico selezionando\n            'Invia notifica' e salvando l'articolo.\n            ", max_length=4, null=True, verbose_name='Notifica via email')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Autore')),
            ],
            options={
                'verbose_name': 'Articolo',
                'verbose_name_plural': 'Articoli',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='UUIDTaggedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.UUIDField(db_index=True, verbose_name='object ID')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_uuidtaggeditem_tagged_items', to='contenttypes.contenttype', verbose_name='content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_uuidtaggeditem_items', to='taggit.tag')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorie',
            },
        ),
        migrations.CreateModel(
            name='UserUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/articles/users/', verbose_name='Immagine')),
                ('body', models.TextField(help_text='Scrivi qualcosa.', verbose_name='Testo')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_uploads', to='blog.article')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Utente')),
            ],
            options={
                'verbose_name': 'Contributo',
                'verbose_name_plural': 'Contributi',
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='Lista di categorie separate da virgole', through='blog.UUIDTaggedItem', to='taggit.Tag', verbose_name='Categorie'),
        ),
    ]
