# Generated by Django 4.2.7 on 2023-12-13 00:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_event_primary_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_id',
            field=models.CharField(default=uuid.uuid4, max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]
