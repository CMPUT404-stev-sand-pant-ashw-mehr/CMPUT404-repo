# Generated by Django 3.2.8 on 2021-10-29 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('author', '0007_alter_author_url'),
        ('post', '0011_alter_post_id'),
        ('comment', '0009_alter_comment_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.CharField(default='7399ab10a1164c9b940b2e4c470c437f', max_length=255, primary_key=True, serialize=False)),
                ('type', models.CharField(default='Like', max_length=255)),
                ('object', models.CharField(max_length=255)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='author.author')),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comment.comment')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
            options={
                'unique_together': {('author', 'comment'), ('author', 'post')},
            },
        ),
    ]
