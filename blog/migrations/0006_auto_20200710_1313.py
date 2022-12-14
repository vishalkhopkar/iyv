# Generated by Django 3.0.7 on 2020-07-10 07:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200710_1036'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'get_latest_by': ['-date_time'], 'ordering': ['-likesCnt']},
        ),
        migrations.AlterField(
            model_name='myuser',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2020, 7, 10, 7, 43, 27, 737670, tzinfo=utc)),
        ),
    ]
