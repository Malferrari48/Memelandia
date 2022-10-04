# Generated by Django 4.0.4 on 2022-05-31 20:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(default='Titel', max_length=30)),
                ('picture', models.ImageField(default='/static/img/default.png', upload_to='C:\\Users\\malfi\\Desktop\\Memelandia\\media')),
                ('title_html', models.CharField(default='Titel', editable=False, max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
