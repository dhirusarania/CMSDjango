# Generated by Django 2.2 on 2020-03-03 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customCMS', '0018_auto_20200211_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaticComponents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('button', models.CharField(max_length=50)),
                ('bgimage', models.ImageField(blank=True, null=True, upload_to='static_components')),
            ],
        ),
    ]