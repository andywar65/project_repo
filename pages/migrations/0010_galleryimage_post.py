# Generated by Django 3.1.2 on 2020-10-21 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20201021_2014'),
        ('pages', '0009_auto_20201020_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='post',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_image', to='blog.article'),
        ),
    ]
