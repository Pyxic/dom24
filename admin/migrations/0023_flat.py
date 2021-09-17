# Generated by Django 3.2.6 on 2021-09-14 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0022_rename_title_level_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.DecimalField(decimal_places=0, max_digits=6, verbose_name='Номер квартиры')),
                ('area', models.FloatField(verbose_name='Площадь (кв.м.)')),
                ('owner', models.IntegerField(blank=True, null=True, verbose_name='Владелец')),
                ('bank_book', models.IntegerField(blank=True, null=True, verbose_name='Лицевой счет')),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin.level', verbose_name='Этаж')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin.section', verbose_name='Секция')),
                ('tariff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin.tariff', verbose_name='Тариф')),
            ],
        ),
    ]
