# Generated by Django 3.0.2 on 2020-01-28 09:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseApp', '0008_productratingsandreviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='productratingsandreviews',
            name='added_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]