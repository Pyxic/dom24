# Generated by Django 3.2.6 on 2021-09-14 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0023_flat'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='house',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='admin.house', verbose_name='Дом'),
            preserve_default=False,
        ),
    ]
