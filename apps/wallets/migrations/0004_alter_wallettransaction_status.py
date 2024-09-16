# Generated by Django 4.2.16 on 2024-09-16 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0003_alter_wallettransaction_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallettransaction',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('INSUFFICIENT_FUNDS', 'INSUFFICIENT_FUNDS'), ('COMPLETED', 'COMPLETED')], default='PENDING', max_length=18),
        ),
    ]
