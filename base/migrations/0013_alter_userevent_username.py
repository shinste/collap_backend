# Generated by Django 4.2.4 on 2023-10-11 22:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_userevent_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userevent',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.user'),
        ),
    ]
