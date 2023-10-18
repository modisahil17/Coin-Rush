# Generated by Django 4.2.6 on 2023-10-18 17:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coinRush', '0012_alter_transaction_transaction_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('sub_title', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=1000)),
                ('publish_datetime', models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 18, 17, 29, 28, 298343, tzinfo=datetime.timezone.utc)),
        ),
    ]
