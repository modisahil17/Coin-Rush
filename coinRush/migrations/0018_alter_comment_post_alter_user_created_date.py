# Generated by Django 4.2.5 on 2023-10-27 18:02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coinRush', '0017_alter_coursecategory_options_alter_learn_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coinRush.post'),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 27, 18, 2, 14, 322281, tzinfo=datetime.timezone.utc)),
        ),
    ]
