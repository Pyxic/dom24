from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField("Телефон", max_length=15, null=True, blank=True)

    class Role(models.TextChoices):
        director = 'директор', _('директор')
        manager = 'управляющий', _('управляющий')
        accountant = 'бухгалтер', _('бухгалтер')
        electriсian = 'электрик', _('электрик')
        plumber = 'сантехник', _('сантехник')

    class Status(models.TextChoices):
        active = 'активен', _('активен')
        new = 'новый', _('новый')
        disabled = 'отключен', _('отключен')

    role = models.CharField("Роль", choices=Role.choices, max_length=20, default='директор')
    status = models.CharField("Статус", choices=Status.choices, max_length=20, default='новый')
