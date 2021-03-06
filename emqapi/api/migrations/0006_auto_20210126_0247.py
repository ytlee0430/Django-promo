# Generated by Django 3.1.5 on 2021-01-26 02:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210126_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerpromocode',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerpromocode',
            name='customer_code',
            field=models.CharField(max_length=16),
        ),
    ]
