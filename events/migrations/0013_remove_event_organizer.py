# Generated by Django 2.2.5 on 2020-09-20 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20200920_1429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='organizer',
        ),
    ]
