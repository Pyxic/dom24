# Generated by Django 3.2.6 on 2021-09-24 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20210915_1642'),
        ('admin', '0043_alter_tariffservice_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('type', models.CharField(choices=[('Любой специалист', 'Любой специалист'), ('Сантехник', 'Сантехник'), ('Электрик', 'Электрик'), ('Слесарь', 'Слесарь')], max_length=30, verbose_name='Тип мастера')),
                ('status', models.CharField(choices=[('новое', 'новое'), ('в процессе', 'в процессе'), ('выполнено', 'выполнено')], max_length=30, verbose_name='Статус')),
                ('description', models.TextField(verbose_name='Описание')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('flat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.flat', verbose_name='Квартира')),
                ('master', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.profile')),
            ],
        ),
    ]
