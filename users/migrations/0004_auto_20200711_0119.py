# Generated by Django 3.0.7 on 2020-07-10 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_articlecnt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profilePic',
            field=models.BooleanField(default=False),
        ),
    ]
