# Generated by Django 3.2.6 on 2021-09-15 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='created',
            field=models.DateField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
    ]
