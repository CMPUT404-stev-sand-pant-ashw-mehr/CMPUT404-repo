# Generated by Django 3.2.8 on 2021-11-15 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0005_alter_like_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='id',
            field=models.CharField(default='0d433a8163fd4bda95334ffd52241e3b', max_length=255, primary_key=True, serialize=False),
        ),
    ]