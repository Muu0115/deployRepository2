# Generated by Django 4.2.8 on 2024-02-10 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_dailyweight'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='target',
            field=models.CharField(default='未設定', max_length=255),
        ),
    ]
