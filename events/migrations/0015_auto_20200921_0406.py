# Generated by Django 2.2.5 on 2020-09-21 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_event_organizer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateField(),
        ),
    ]
