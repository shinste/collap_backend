# Generated by Django 4.2.4 on 2023-09-07 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(),
        ),
        migrations.DeleteModel(
            name='EventDates',
        ),
    ]