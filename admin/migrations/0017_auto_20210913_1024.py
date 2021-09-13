# Generated by Django 3.2.6 on 2021-09-13 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0016_house_level_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='house/', verbose_name='Изображение #1. Размер: (522x350)'),
        ),
        migrations.AddField(
            model_name='house',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='house/', verbose_name='Изображение #2. Размер: (248x160)'),
        ),
        migrations.AddField(
            model_name='house',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='house/', verbose_name='Изображение #3. Размер: (248x160)'),
        ),
        migrations.AddField(
            model_name='house',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to='house/', verbose_name='Изображение #4. Размер: (248x160)'),
        ),
        migrations.AddField(
            model_name='house',
            name='image5',
            field=models.ImageField(blank=True, null=True, upload_to='house/', verbose_name='Изображение #5. Размер: (248x160)'),
        ),
    ]
