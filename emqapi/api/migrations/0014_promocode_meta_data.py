# Generated by Django 3.1.5 on 2021-01-27 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20210126_0341'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='meta_data',
            field=models.JSONField(default={}),
        ),
    ]