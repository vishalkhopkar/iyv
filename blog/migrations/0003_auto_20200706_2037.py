# Generated by Django 3.0.7 on 2020-07-06 15:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200706_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2020, 7, 6, 15, 7, 39, 468075, tzinfo=utc)),
        ),
    ]
