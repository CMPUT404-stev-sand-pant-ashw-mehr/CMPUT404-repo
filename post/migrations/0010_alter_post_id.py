# Generated by Django 3.2.8 on 2021-10-29 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_alter_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.CharField(default='958fa856fd1d42b89138a08a8a02bbcd', max_length=255, primary_key=True, serialize=False),
        ),
    ]
