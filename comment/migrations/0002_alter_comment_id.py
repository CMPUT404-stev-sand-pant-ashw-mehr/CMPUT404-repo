# Generated by Django 3.2.8 on 2021-10-29 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.CharField(default='ca09b4626f844826b0fb02d1ba374ce8', editable=False, max_length=255, primary_key=True, serialize=False),
        ),
    ]
