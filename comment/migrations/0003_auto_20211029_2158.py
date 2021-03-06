# Generated by Django 3.2.8 on 2021-10-29 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_alter_post_id'),
        ('comment', '0002_alter_comment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.CharField(default='361d1a4e23b74119943eb5d6716f7099', editable=False, max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together={('id', 'post')},
        ),
    ]
