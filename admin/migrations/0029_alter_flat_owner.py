# Generated by Django 3.2.6 on 2021-09-15 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_owner'),
        ('admin', '0028_alter_flat_house'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flat',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.owner', verbose_name='Владелец'),
        ),
    ]
