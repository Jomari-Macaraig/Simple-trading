# Generated by Django 4.2.16 on 2024-09-16 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='running_balance',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=32),
        ),
    ]
