# Generated by Django 3.2.6 on 2021-09-17 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0029_alter_flat_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indication', models.FloatField(verbose_name='Текущие показания')),
                ('status', models.CharField(choices=[('новое', 'новое'), ('учтено', 'учтено'), ('учтено и оплачено', 'учтено и оплачено'), ('нулевое', 'нулевое')], max_length=20, verbose_name='Статус')),
                ('flat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.flat', verbose_name='Квартира')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.service', verbose_name='Услуга')),
            ],
        ),
    ]
