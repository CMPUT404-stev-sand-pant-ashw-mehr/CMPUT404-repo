# Generated by Django 3.2.8 on 2021-10-28 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='type',
            field=models.CharField(default='author', max_length=255),
        ),
    ]