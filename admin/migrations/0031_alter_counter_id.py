# Generated by Django 3.2.6 on 2021-09-17 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0030_counter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='id',
            field=models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='№'),
        ),
    ]
