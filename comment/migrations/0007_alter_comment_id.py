# Generated by Django 3.2.8 on 2021-11-15 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0006_alter_comment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.CharField(default='7927e4f7f6064632b54c159938b57b11', editable=False, max_length=255, primary_key=True, serialize=False),
        ),
    ]
