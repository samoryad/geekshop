# Generated by Django 3.1.3 on 2021-01-08 18:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0011_auto_20210108_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 10, 18, 5, 31, 895334, tzinfo=utc)),
        ),
    ]
