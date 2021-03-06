# Generated by Django 3.2.6 on 2021-09-15 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_owner_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='owners/', verbose_name='Сменить изображение'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='О владельце (заметки)'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='identify',
            field=models.DecimalField(decimal_places=0, max_digits=6, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='telegram',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Telegram'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='viber',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Viber'),
        ),
    ]
