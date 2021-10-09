# Generated by Django 3.2.6 on 2021-09-27 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20210915_1642'),
        ('admin', '0044_masterrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterrequest',
            name='master',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.profile', verbose_name='Мастер'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст сообщения')),
                ('has_debt', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('flat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin.flat', verbose_name='Квартира')),
                ('house', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin.house', verbose_name='ЖК')),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin.level', verbose_name='Этаж')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin.section', verbose_name='Секция')),
            ],
        ),
    ]