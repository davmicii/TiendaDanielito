# Generated by Django 5.0.6 on 2024-07-02 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0003_subcategoria'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subcategoria',
            options={'ordering': ['id'], 'verbose_name': 'SubCategoria', 'verbose_name_plural': 'SubCategorias'},
        ),
        migrations.AlterModelTable(
            name='subcategoria',
            table='subcategoria',
        ),
    ]
