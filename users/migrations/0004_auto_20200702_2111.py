# Generated by Django 3.0.6 on 2020-07-02 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200403_1039'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('last_name', 'first_name', 'username')},
        ),
        migrations.AddField(
            model_name='profile',
            name='is_trusted',
            field=models.BooleanField(default=False, verbose_name='Di fiducia'),
        ),
    ]