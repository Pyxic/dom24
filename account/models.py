from django.conf import settings
from django.db import models
from django.urls import reverse_lazy, reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
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

    def __str__(self):
        return self.role + ' - ' + self.user.first_name + ' ' + self.user.last_name


class Owner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField("Сменить изображение", upload_to='owners/', null=True, blank=True)
    patronymic = models.CharField("Отчество", max_length=100)
    birthday = models.DateField("Дата рождения")
    phone = models.CharField("Телефон", max_length=15)
    viber = models.CharField("Viber", max_length=50, null=True, blank=True)
    telegram = models.CharField("Telegram", max_length=50, null=True, blank=True)
    identify = models.DecimalField("ID", max_digits=6, decimal_places=0, unique=True)
    created = models.DateField(auto_now_add=True)
    description = models.TextField("О владельце (заметки)", null=True, blank=True)

    class Status(models.TextChoices):
        active = 'активен', _('активен')
        new = 'новый', _('новый')
        disabled = 'отключен', _('отключен')
        __empty__ = _('')

    status = models.CharField("Статус", choices=Status.choices, max_length=20, default='новый')

    def fullname(self):
        return f"{self.user.last_name} {self.user.first_name} {self.patronymic}"

    def houses_str(self):
        flats = self.flat_set.all().distinct('house_id')
        houses = []
        for flat in flats:
            houses.append('<a href="' + reverse('admin:detail_house', args=[flat.house.pk]) + '">' +
                          flat.house.name+'</a>')
        answer = '<br>'.join(houses)
        return mark_safe(answer)

    def flats_str(self):
        flats = self.flat_set.all()
        answer = []
        for flat in flats:
            answer.append('<a href="">№' + str(flat.number) + ' ' + flat.house.name + '</a>')
        return mark_safe('<br>'.join(answer))

    def __str__(self):
        return self.fullname()

    def has_debt(self):
        flats = self.flat_set.all()
        for flat in flats:
            if flat.balance() < 0:
                return True
            else:
                return False


class PermissionPage(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.id)


class PermissionUrl(models.Model):
    page = models.ForeignKey(PermissionPage, on_delete=models.CASCADE)
    url = models.CharField(max_length=250)


class PermissionAccess(models.Model):
    page = models.ForeignKey(PermissionPage, on_delete=models.SET_NULL, null=True)
    access = models.BooleanField()
    role = models.CharField(choices=Profile.Role.choices, max_length=100)
