# Generated by Django 3.2.8 on 2021-11-15 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0008_alter_comment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.CharField(editable=False, max_length=255, primary_key=True, serialize=False),
        ),
    ]
