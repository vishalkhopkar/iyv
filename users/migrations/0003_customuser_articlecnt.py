# Generated by Django 3.0.7 on 2020-07-10 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='articleCnt',
            field=models.IntegerField(default=0),
        ),
    ]