# Generated by Django 3.2.8 on 2021-11-15 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('author', '0001_initial'),
        ('post', '0008_alter_post_id'),
        ('followers', '0001_initial'),
        ('comment', '0009_alter_comment_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='inbox', max_length=10)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='author.author')),
                ('comment_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inbox_comment', to='comment.comment')),
                ('follow_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inbox_request', to='followers.friendrequest')),
                ('post_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inbox_post', to='post.post')),
            ],
        ),
        migrations.AddConstraint(
            model_name='inbox',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('post_item__isnull', False), ('comment_item__isnull', True), ('follow_item__isnull', True)), models.Q(('post_item__isnull', True), ('comment_item__isnull', False), ('follow_item__isnull', True)), models.Q(('post_item__isnull', True), ('comment_item__isnull', True), ('follow_item__isnull', False)), _connector='OR'), name='only_one_item_type'),
        ),
    ]