# Generated by Django 3.2.8 on 2021-10-29 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_alter_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.CharField(default='2fab8e530e594588b01f260bb8b2fdd9', max_length=255, primary_key=True, serialize=False),
        ),
    ]
