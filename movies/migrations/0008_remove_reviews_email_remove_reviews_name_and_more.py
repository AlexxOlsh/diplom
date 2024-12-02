# Generated by Django 5.1.3 on 2024-11-30 15:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_rename_favorites_movie_favourites'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviews',
            name='email',
        ),
        migrations.RemoveField(
            model_name='reviews',
            name='name',
        ),
        migrations.RemoveField(
            model_name='reviews',
            name='parent',
        ),
        migrations.AddField(
            model_name='reviews',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
            preserve_default=False,
        ),
    ]