# Generated by Django 3.2.8 on 2021-10-24 06:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('author', '0003_alter_author_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='local_user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='author',
            unique_together={('id', 'local_user_id')},
        ),
    ]
