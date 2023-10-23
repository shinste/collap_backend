# Generated by Django 4.2.4 on 2023-10-09 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_eventdate_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEvent',
            fields=[
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='base.event')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.user')),
            ],
            options={
                'unique_together': {('event_id', 'username')},
            },
        ),
    ]