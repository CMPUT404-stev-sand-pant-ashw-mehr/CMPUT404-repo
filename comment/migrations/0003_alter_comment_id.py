# Generated by Django 3.2.8 on 2021-10-29 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_alter_comment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.CharField(default='3055c36fcd1644cab8bf97e042efce69', editable=False, max_length=255, primary_key=True, serialize=False),
        ),
    ]