# Generated by Django 4.2.6 on 2023-10-13 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coinRush', '0004_alter_user_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(default='2023-10-13 21:35:17'),
        ),
    ]
