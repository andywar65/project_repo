# Generated by Django 3.0.4 on 2020-03-20 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagine', '0005_remove_blog_fb_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutional',
            name='slug',
            field=models.SlugField(null=True, verbose_name='Slug'),
        ),
        migrations.AddField(
            model_name='institutional',
            name='summary',
            field=models.BooleanField(default=True, verbose_name='Mostra sommario'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='notice',
            field=models.CharField(blank=True, choices=[('NOSP', 'Non inviare'), ('SPAM', 'Da inviare'), ('DONE', 'Già inviata')], help_text="Invia notifica in automatico selezionando\n            'Invia notifica' e salvando l'articolo.\n            ", max_length=4, null=True, verbose_name='Notifica via email'),
        ),
    ]