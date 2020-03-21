# Generated by Django 3.0.4 on 2020-03-21 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20200321_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treepage',
            name='slug',
            field=models.SlugField(help_text="Titolo come appare nell'indirizzo della pagina,\n            solo lettere minuscole e senza spazi", null=True, verbose_name='Slug'),
        ),
    ]
