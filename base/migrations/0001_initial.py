# Generated by Django 4.2.4 on 2023-10-30 21:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.CharField(default=uuid.uuid4, max_length=8, primary_key=True, serialize=False, unique=True)),
                ('primary_date', models.DateField()),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('username', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.event')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.user')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.CharField(max_length=500)),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.event')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.user')),
            ],
        ),
        migrations.CreateModel(
            name='EventUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.event')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.user')),
            ],
        ),
        migrations.CreateModel(
            name='EventDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.event')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.user'),
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.event')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.user')),
            ],
        ),
        migrations.AddConstraint(
            model_name='vote',
            constraint=models.UniqueConstraint(fields=('event_id', 'username'), name='unique_vote'),
        ),
        migrations.AddConstraint(
            model_name='notification',
            constraint=models.UniqueConstraint(fields=('event_id', 'username', 'notification'), name='unique_notification'),
        ),
        migrations.AddConstraint(
            model_name='eventuser',
            constraint=models.UniqueConstraint(fields=('event_id', 'username'), name='unique_userevent'),
        ),
        migrations.AlterUniqueTogether(
            name='eventuser',
            unique_together={('event_id', 'username')},
        ),
        migrations.AddConstraint(
            model_name='eventdate',
            constraint=models.UniqueConstraint(fields=('event_id', 'date'), name='unique_event_date'),
        ),
        migrations.AlterUniqueTogether(
            name='eventdate',
            unique_together={('event_id', 'date')},
        ),
        migrations.AddConstraint(
            model_name='availability',
            constraint=models.UniqueConstraint(fields=('event_id', 'username', 'date'), name='unique_availability'),
        ),
    ]
