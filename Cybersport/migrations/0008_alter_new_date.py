# Generated by Django 4.0.2 on 2022-07-04 17:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Cybersport', '0007_alter_new_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 4, 17, 48, 24, 743445, tzinfo=utc)),
        ),
    ]