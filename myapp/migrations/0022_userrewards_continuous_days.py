# Generated by Django 4.2.8 on 2024-02-29 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_alter_healthrecord_sleep_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrewards',
            name='continuous_days',
            field=models.IntegerField(default=0),
        ),
    ]