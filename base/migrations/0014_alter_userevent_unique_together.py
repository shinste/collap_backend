# Generated by Django 4.2.4 on 2023-10-11 23:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_userevent_username'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userevent',
            unique_together={('event_id', 'username')},
        ),
    ]
