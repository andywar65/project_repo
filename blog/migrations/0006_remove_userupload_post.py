# Generated by Django 3.1.2 on 2020-10-21 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20201021_2014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userupload',
            name='post',
        ),
    ]