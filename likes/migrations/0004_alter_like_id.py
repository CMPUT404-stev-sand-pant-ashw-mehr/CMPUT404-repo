# Generated by Django 3.2.8 on 2021-10-29 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0003_alter_like_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='id',
            field=models.CharField(default='cf46d754c1e04c448b357ade50498e3e', max_length=255, primary_key=True, serialize=False),
        ),
    ]
