# Generated by Django 3.2.6 on 2021-09-15 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_owner_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='description',
            field=models.TextField(default=1, verbose_name='О владельце (заметки)'),
            preserve_default=False,
        ),
    ]
