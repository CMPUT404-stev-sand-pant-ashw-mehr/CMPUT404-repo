# Generated by Django 3.2.8 on 2021-10-29 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.CharField(default='c673cfc01ffc4eb7810683e4cf20ba2e', max_length=255, primary_key=True, serialize=False),
        ),
    ]
