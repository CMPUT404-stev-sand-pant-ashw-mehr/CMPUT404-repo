# Generated by Django 3.2.8 on 2021-10-29 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.CharField(default='17e2bf64-4f20-4db4-a88c-df922dbb38c1', max_length=255, primary_key=True, serialize=False),
        ),
    ]