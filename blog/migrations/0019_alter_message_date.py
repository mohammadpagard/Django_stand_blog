# Generated by Django 3.2 on 2022-07-06 13:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20220703_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 6, 13, 38, 50, 444740, tzinfo=utc)),
        ),
    ]
