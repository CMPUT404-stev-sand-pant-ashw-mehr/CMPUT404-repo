# Generated by Django 3.2.8 on 2021-10-29 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_alter_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.CharField(default='45f00887e5a747918ab689b4cc777793', max_length=255, primary_key=True, serialize=False),
        ),
    ]
