# Generated by Django 3.1.5 on 2021-01-26 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210126_0259'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='customerpromocode',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='customerpromocode',
            constraint=models.UniqueConstraint(fields=('customer_code', 'promo_code', 'transfer'), name='customer promo constraint'),
        ),
    ]
