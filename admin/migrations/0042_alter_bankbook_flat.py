# Generated by Django 3.2.6 on 2021-09-22 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0041_remove_flat_bank_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankbook',
            name='flat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin.flat', verbose_name='Квартира'),
        ),
    ]
