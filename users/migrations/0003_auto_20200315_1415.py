# Generated by Django 3.0.4 on 2020-03-15 13:15

from django.db import migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200314_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=filebrowser.fields.FileBrowseField(blank=True, max_length=200, null=True, verbose_name='Avatar'),
        ),
    ]