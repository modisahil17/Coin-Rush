# Generated by Django 4.2.5 on 2023-10-27 18:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coinRush', '0018_alter_comment_post_alter_user_created_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_comments',
        ),
        migrations.AlterField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 27, 18, 11, 20, 853725, tzinfo=datetime.timezone.utc)),
        ),
    ]