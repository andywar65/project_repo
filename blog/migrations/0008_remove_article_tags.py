# Generated by Django 3.1.2 on 2020-10-25 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_userupload_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='tags',
        ),
    ]