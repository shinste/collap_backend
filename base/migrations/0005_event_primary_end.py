# Generated by Django 4.2.7 on 2023-12-08 19:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_event_end_event_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='primary_end',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
