# Generated by Django 3.2.8 on 2021-10-29 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_alter_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.CharField(default='731c4403647b446ea2e73a107ac574c4', max_length=255, primary_key=True, serialize=False),
        ),
    ]
