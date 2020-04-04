# Generated by Django 2.2 on 2020-03-27 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customCMS', '0015_homecomponents'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaticComponents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Section Title', max_length=50)),
                ('name', models.CharField(help_text='Identifier', max_length=50)),
                ('content', models.TextField()),
                ('button', models.CharField(max_length=50)),
                ('button_url', models.URLField(max_length=250)),
                ('bgimage', models.ImageField(blank=True, null=True, upload_to='static_components')),
            ],
        ),
        migrations.AddField(
            model_name='homecms',
            name='header_text_3',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]