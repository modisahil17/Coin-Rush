# Generated by Django 4.2.5 on 2023-11-16 20:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coinRush', '0004_alter_user_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 16, 20, 18, 14, 513543, tzinfo=datetime.timezone.utc)),
        ),
    ]