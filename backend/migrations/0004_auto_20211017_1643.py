# Generated by Django 3.2.8 on 2021-10-17 22:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0003_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('commentType', models.CharField(default='comment', max_length=255)),
                ('comment', models.TextField()),
                ('contentType', models.CharField(max_length=255)),
                ('published', models.DateTimeField(default='2021-10-17T16:43:45-06:00')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.post')),
            ],
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
    ]
