# Generated by Django 3.1.5 on 2021-01-26 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210125_0928'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='customerpromocode',
            unique_together={('promo_code', 'promo_code', 'transfer')},
        ),
    ]
