# Generated by Django 4.2.5 on 2023-10-26 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_userevent_id_alter_userevent_event_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventdate',
            name='id',
            field=models.BigAutoField(auto_created=True, default=2, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventdate',
            name='event_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.event'),
        ),
        migrations.AddConstraint(
            model_name='eventdate',
            constraint=models.UniqueConstraint(fields=('event_id', 'date'), name='unique_event_date'),
        ),
    ]
