# Generated by Django 3.2.8 on 2021-10-29 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_alter_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.CharField(default='13d61c94637741229f86e94f3b74a1cc', max_length=255, primary_key=True, serialize=False),
        ),
    ]