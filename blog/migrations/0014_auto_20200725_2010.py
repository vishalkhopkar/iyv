# Generated by Django 3.0.7 on 2020-07-25 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20200722_0110'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='isReported',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='reportReasons',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
