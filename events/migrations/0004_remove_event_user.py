# Generated by Django 4.0 on 2023-02-10 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_event_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='user',
        ),
    ]
