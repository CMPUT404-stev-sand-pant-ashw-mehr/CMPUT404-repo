# Generated by Django 3.2.8 on 2021-11-19 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0003_remove_author_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
