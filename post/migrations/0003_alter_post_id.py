# Generated by Django 3.2.8 on 2021-10-29 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_alter_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.CharField(default='8a8a41f5fcfe4b8fab931730dff4793d', max_length=255, primary_key=True, serialize=False),
        ),
    ]
