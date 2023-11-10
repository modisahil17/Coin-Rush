# Generated by Django 4.2.5 on 2023-11-10 18:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coinRush', '0022_post_views_alter_user_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 10, 18, 59, 34, 151535, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='userholding',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='NewsComments',
        ),
    ]