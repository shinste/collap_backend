# Generated by Django 4.2.7 on 2023-11-29 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_notification_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='name',
        ),
    ]
