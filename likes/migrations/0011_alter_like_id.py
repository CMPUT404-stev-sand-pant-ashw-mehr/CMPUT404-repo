# Generated by Django 3.2.8 on 2021-11-23 05:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0010_alter_like_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]