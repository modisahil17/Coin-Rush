# Generated by Django 4.2.5 on 2023-11-17 03:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coinRush', '0006_alter_learn_image_alter_user_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 17, 3, 0, 24, 596090, tzinfo=datetime.timezone.utc)),
        ),
    ]
