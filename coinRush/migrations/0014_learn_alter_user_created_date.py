# Generated by Django 4.2.6 on 2023-10-19 01:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coinRush', '0013_news_alter_user_created_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Learn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('external_link', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 19, 1, 19, 41, 74795, tzinfo=datetime.timezone.utc)),
        ),
    ]
