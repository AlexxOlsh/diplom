# Generated by Django 5.1.3 on 2024-11-30 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_movie_favorites'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='favorites',
            new_name='favourites',
        ),
    ]
