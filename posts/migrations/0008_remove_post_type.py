# Generated by Django 4.0 on 2023-02-26 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_remove_comment_has_photo_remove_comment_link_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='type',
        ),
    ]
