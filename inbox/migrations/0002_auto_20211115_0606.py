# Generated by Django 3.2.8 on 2021-11-15 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0007_alter_like_id'),
        ('inbox', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='inbox',
            name='only_one_item_type',
        ),
        migrations.RemoveField(
            model_name='inbox',
            name='comment_item',
        ),
        migrations.AddField(
            model_name='inbox',
            name='like_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inbox_like', to='likes.like'),
        ),
        migrations.AddConstraint(
            model_name='inbox',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('post_item__isnull', False), ('like_item__isnull', True), ('follow_item__isnull', True)), models.Q(('post_item__isnull', True), ('like_item__isnull', False), ('follow_item__isnull', True)), models.Q(('post_item__isnull', True), ('like_item__isnull', True), ('follow_item__isnull', False)), _connector='OR'), name='only_one_item_type'),
        ),
    ]
