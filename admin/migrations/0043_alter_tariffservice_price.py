# Generated by Django 3.2.6 on 2021-09-22 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0042_alter_bankbook_flat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tariffservice',
            name='price',
            field=models.FloatField(verbose_name='Цена'),
        ),
    ]
