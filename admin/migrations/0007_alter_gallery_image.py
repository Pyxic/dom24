# Generated by Django 3.2.6 on 2021-08-20 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0006_alter_gallery_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=models.ImageField(default=12323, upload_to='gallery/%Y/%m/%d', verbose_name='Изображение'),
            preserve_default=False,
        ),
    ]
