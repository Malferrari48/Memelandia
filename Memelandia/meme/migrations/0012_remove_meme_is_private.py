# Generated by Django 4.0.5 on 2022-07-03 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meme', '0011_meme_is_private'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meme',
            name='is_private',
        ),
    ]
