# Generated by Django 3.2.8 on 2021-11-15 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_alter_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.CharField(default='0845b10ad5714642a2da4bd25c19331c', max_length=255, primary_key=True, serialize=False),
        ),
    ]
