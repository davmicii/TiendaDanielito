# Generated by Django 5.0.6 on 2024-08-07 00:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0014_pago'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pago',
            options={'ordering': ['id'], 'verbose_name': 'Pago', 'verbose_name_plural': 'Pagos'},
        ),
        migrations.AlterModelTable(
            name='pago',
            table='pago',
        ),
    ]
