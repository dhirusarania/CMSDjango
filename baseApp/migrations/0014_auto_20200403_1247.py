# Generated by Django 2.2 on 2020-04-03 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseApp', '0013_startup_pitch_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updates',
            name='added_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='updates',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]