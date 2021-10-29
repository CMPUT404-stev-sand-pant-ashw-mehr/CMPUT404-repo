# Generated by Django 3.2.8 on 2021-10-29 01:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='type',
            field=models.CharField(default='author', max_length=255),
        ),
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=255, primary_key=True, serialize=False, unique=True),
        ),
    ]