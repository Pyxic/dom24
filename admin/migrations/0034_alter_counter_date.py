# Generated by Django 3.2.6 on 2021-09-17 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0033_alter_flat_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='date',
            field=models.DateField(),
        ),
    ]
