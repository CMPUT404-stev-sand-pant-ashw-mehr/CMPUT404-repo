# Generated by Django 3.2.8 on 2021-10-27 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
        ('followers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followers',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='author.author'),
        ),
        migrations.AlterField(
            model_name='followers',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='author.author'),
        ),
    ]