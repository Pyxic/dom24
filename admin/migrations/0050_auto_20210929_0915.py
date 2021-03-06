# Generated by Django 3.2.6 on 2021-09-29 06:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin', '0049_alter_cashbox_payment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='from_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='counter',
            name='status',
            field=models.CharField(choices=[(None, ''), ('новое', 'новое'), ('учтено', 'учтено'), ('учтено и оплачено', 'учтено и оплачено'), ('нулевое', 'нулевое')], max_length=20, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='masterrequest',
            name='status',
            field=models.CharField(choices=[(None, ''), ('новое', 'новое'), ('в процессе', 'в процессе'), ('выполнено', 'выполнено')], max_length=30, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='masterrequest',
            name='type',
            field=models.CharField(choices=[(None, ''), ('Любой специалист', 'Любой специалист'), ('Сантехник', 'Сантехник'), ('Электрик', 'Электрик'), ('Слесарь', 'Слесарь')], max_length=30, verbose_name='Тип мастера'),
        ),
    ]
