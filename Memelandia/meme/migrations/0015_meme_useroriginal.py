# Generated by Django 4.0.5 on 2022-07-07 21:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meme', '0014_remove_meme_is_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='meme',
            name='userOriginal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_original', to=settings.AUTH_USER_MODEL),
        ),
    ]
