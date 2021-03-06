# Generated by Django 3.2.6 on 2021-08-18 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_auto_20210811_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutus',
            name='additional_description',
            field=models.TextField(blank=True, null=True, verbose_name='Краткий текст'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='additional_title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Краткое текст'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Заголовок'),
        ),
    ]
