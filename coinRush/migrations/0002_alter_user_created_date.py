# Generated by Django 4.2.5 on 2023-11-20 04:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coinRush', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 20, 4, 14, 9, 279589, tzinfo=datetime.timezone.utc)),
        ),
    ]
