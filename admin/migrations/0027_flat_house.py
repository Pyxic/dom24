# Generated by Django 3.2.6 on 2021-09-14 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0026_remove_flat_house'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='house',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='admin.house', verbose_name='Дом'),
        ),
    ]
