# Generated by Django 3.0.7 on 2020-07-18 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200711_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profilePicFileName',
            field=models.CharField(default='dp.jpg', max_length=30),
            preserve_default=False,
        ),
    ]
