import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum, Avg, Max, Min
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
from account.models import Profile, Owner
from admin.singleton import SingletonModel
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class SeoText(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    keywords = models.TextField()


class MainPage(SingletonModel):
    title = models.CharField("Заголовок", max_length=100, null=True, blank=True)
    description = models.TextField("Краткий текст")
    show_link = models.BooleanField("Показывать ссылки на приложения")
    seo = models.ForeignKey(SeoText, on_delete=models.SET_NULL, null=True)
    image_gallery = GenericRelation('gallery')


class NearBlock(models.Model):
    image = models.ImageField("Изображение", upload_to='near/%Y/%m/%d')
    title = models.CharField("Заголовок блока", max_length=100)
    description = models.TextField("Описание", max_length=300)


class AboutUs(SingletonModel):
    title = models.CharField("Заголовок", max_length=100, null=True, blank=True)
    description = models.TextField("Краткое текст", null=True, blank=True)
    image = models.ImageField("Изображение", upload_to='about')
    additional_title = models.CharField("Заголовок", max_length=100, null=True, blank=True)
    additional_description = models.TextField("Краткий текст", null=True, blank=True)
    seo = models.ForeignKey(SeoText, on_delete=models.SET_NULL, null=True)


class Document(models.Model):
    name = models.CharField("Название", max_length=30)
    file = models.FileField(upload_to='documents/%Y/%m/%d')

    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super().delete(*args, **kwargs)


class ServicePage(SingletonModel):
    seo = models.ForeignKey(SeoText, on_delete=models.SET_NULL, null=True)


class CustomerService(models.Model):
    name = models.CharField("Название услуги", max_length=100)
    description = models.TextField("Описание услуги")
    image = models.ImageField("Изображение", upload_to='customer_services/%Y/%m/%d')


class ContactPage(SingletonModel):
    title = models.CharField("Заголовок", max_length=100, null=True, blank=True)
    description = models.TextField("Краткий текст", null=True, blank=True)
    link_commercial = models.CharField("Ссылка на коммерческий сайт", max_length=200, null=True, blank=True)
    fullname = models.CharField("ФИО", max_length=200, null=True, blank=True)
    location = models.CharField("Локация", max_length=100, null=True, blank=True)
    address = models.CharField("Адрес", max_length=100, null=True, blank=True)
    phone = models.CharField("Телефон", max_length=15, null=True, blank=True)
    e_mail = models.EmailField("E-mail", max_length=30, null=True, blank=True)
    map = models.TextField("Код карты", null=True, blank=True)
    seo = models.ForeignKey(SeoText, on_delete=models.SET_NULL, null=True)


class Gallery(models.Model):
    """Галерея изображений для объекта"""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField("Изображение", upload_to='gallery/%Y/%m/%d')
    is_additional = models.BooleanField("Дополнительная галерея", default=False, blank=True)

    def __str__(self):
        return f"Изображения для {self.content_object}"

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галереи'


class Unit(models.Model):
    name = models.CharField("Ед. изм.", max_length=20)

    def __str__(self):
        return self.name


class Service(models.Model):
    """Модель хранит коммунальные услуги"""

    name = models.CharField("Услуга", max_length=50)
    unit = models.ForeignKey(Unit, on_delete=models.RESTRICT, null=True, blank=True)
    show = models.BooleanField("Показывать в счетчиках")

    def __str__(self):
        return self.name


class Tariff(models.Model):
    """Хранит тарифы для жителей"""

    name = models.CharField("Название тарифа", max_length=100)
    description = models.TextField("Описание тарифа")
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class TariffService(models.Model):
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.FloatField("Цена")
    currency = models.CharField("Валюта", default='грн', max_length=5)


class Requisites(SingletonModel):
    name = models.CharField("Название компании", max_length=150)
    information = models.TextField("Информация")


class PaymentItem(models.Model):
    name = models.CharField("Название", max_length=150)

    class Types(models.TextChoices):
        expenses = 'расходы', _('расходы')
        comings = 'приходы', _('приходы')

    type = models.CharField("Приходы/Расходы", choices=Types.choices, max_length=30)

    def __str__(self):
        return self.name


class House(models.Model):
    name = models.CharField("Название", max_length=150)
    address = models.CharField("Адрес", max_length=150)
    image1 = models.ImageField("Изображение #1. Размер: (522x350)", upload_to='house/', null=True, blank=True)
    image2 = models.ImageField("Изображение #2. Размер: (248x160)", upload_to='house/', null=True, blank=True)
    image3 = models.ImageField("Изображение #3. Размер: (248x160)", upload_to='house/', null=True, blank=True)
    image4 = models.ImageField("Изображение #4. Размер: (248x160)", upload_to='house/', null=True, blank=True)
    image5 = models.ImageField("Изображение #5. Размер: (248x160)", upload_to='house/', null=True, blank=True)
    users = models.ManyToManyField(Profile)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('admin:detail_house',
                       args=[self.id])


class Section(models.Model):
    name = models.CharField("Название", max_length=150)
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField("Название", max_length=150)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='house_level')

    def __str__(self):
        return self.name


class Flat(models.Model):
    number = models.CharField("Номер квартиры", max_length=10)
    area = models.FloatField("Площадь (кв.м.)")
    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name='Дом')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, verbose_name="Секция", null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, verbose_name="Этаж", null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, verbose_name='Владелец', null=True, blank=True)
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, verbose_name="Тариф", null=True)

    def balance(self):
        if self.bankbook_set.first():
            return self.bankbook_set.first().balance()
        return '(нет счета)'

    def avg_expenses(self):
        sum_for_month = 0
        max_date = Receipt.objects.filter(flat_id=self.id).aggregate(Max('date__month')).get('date__month__max')
        min_date = Receipt.objects.filter(flat_id=self.id).aggregate(Min('date__month')).get('date__month__min')
        month_count = 0
        logger.info(str(min_date)+" "+str(max_date))
        if not all([max_date, min_date]):
            return '0.00'
        for i in range(min_date, max_date+1):
            receipts = Receipt.objects.filter(flat_id=self.id, date__month=i)
            month_count += 1
            for receipt in receipts:
                sum_for_month += receipt.get_price()
        try:
            return sum_for_month/month_count
        except ZeroDivisionError:
            return sum_for_month

    def __str__(self):
        return str(self.number)


class Counter(models.Model):
    id = models.CharField("№", primary_key=True, max_length=15)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, verbose_name='Квартира')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')
    indication = models.FloatField("Текущие показания")
    date = models.DateField()

    class TypesCounter(models.TextChoices):
        new = 'новое', _('новое')
        taken_into_account = 'учтено', _('учтено')
        paid = 'учтено и оплачено', _('учтено и оплачено')
        zero = 'нулевое', _('нулевое')
        __empty__ = _('')

    status = models.CharField("Статус", choices=TypesCounter.choices, max_length=20)


class BankBook(models.Model):
    id = models.CharField('№', primary_key=True, max_length=15)
    flat = models.ForeignKey(Flat, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Квартира')

    class Status(models.TextChoices):
        active = 'Активен', _('Активен')
        disabled = 'Неактивен', _('Неактивен')
        __empty__ = _('')

    status = models.CharField("Статус", choices=Status.choices, max_length=20)

    def __str__(self):
        return self.id

    def balance(self):
        incomes = self.cashbox_set.filter(type='приход').aggregate(Sum('amount_of_money'))\
            .get('amount_of_money__sum', 0.00)
        receipts = sum([receipt.get_price() for receipt in self.flat.receipt_set.all()])
        logger.info(incomes)
        if incomes:
            return float(incomes)-receipts
        if receipts:
            return 0.00-receipts
        else:
            return 0.00


class CashBox(models.Model):
    id = models.CharField('№', primary_key=True, max_length=15)
    date = models.DateField()
    status = models.BooleanField('Проведен', default=True)
    payment_type = models.ForeignKey(PaymentItem, on_delete=models.RESTRICT, verbose_name='Тип платежа',
                                     null=True, blank=True)
    bankbook = models.ForeignKey(BankBook, on_delete=models.SET_NULL,
                                 null=True, blank=True, verbose_name='Лицевой счет')

    class Types(models.TextChoices):
        income = 'приход', _('приход')
        expense = 'расход', _('расход')
        __empty__ = _('')

    type = models.CharField('Приход/Расход', choices=Types.choices, max_length=10)
    amount_of_money = models.DecimalField('Сумма(грн)', decimal_places=2, max_digits=10)
    manager = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField("Комментарий", null=True, blank=True)


class Receipt(models.Model):
    id = models.CharField("№", primary_key=True, max_length=15)
    date = models.DateField()
    date_from = models.DateField("Период с")
    date_to = models.DateField("Период по")
    flat = models.ForeignKey(Flat, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name="Квартира")
    is_checked = models.BooleanField("Проведена", default=True)
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True,
                               verbose_name='Тариф')

    class Status(models.TextChoices):
        paid = 'оплачена', _('оплачена')
        part = 'частично оплачена', _('частично оплачена')
        unpaid = 'не оплачена', _('не оплачена')
        __empty__ = _('')

    status = models.CharField("Статус", choices=Status.choices, max_length=20)
    services = models.ManyToManyField(Service, through='ReceiptService')

    def get_price(self):
        return self.receiptservice_set.all().aggregate(Sum('price')).get('price__sum', 0.00)


class ReceiptService(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.RESTRICT)
    amount = models.FloatField("Расход")
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    price_unit = models.FloatField("Цеа за 1 ед., грн.")
    price = models.FloatField("Стоимость, грн.")


class MasterRequest(models.Model):
    date = models.DateField()
    time = models.TimeField()
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, verbose_name="Квартира")

    class TypeMaster(models.TextChoices):
        anyone = 'Любой специалист', _('Любой специалист')
        plumber = 'Сантехник', _('Сантехник')
        electrician = 'Электрик', _('Электрик')
        locksmith = 'Слесарь', _('Слесарь')
        __empty__ = _('')

    class Status(models.TextChoices):
        new = 'новое', _('новое')
        process = 'в процессе', _('в процессе')
        complete = 'выполнено', _('выполнено')
        __empty__ = _('')

    type = models.CharField("Тип мастера", choices=TypeMaster.choices, max_length=30)
    status = models.CharField("Статус", choices=Status.choices, max_length=30, default='новое', blank=True)
    master = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Мастер')
    description = models.TextField("Описание")
    comment = models.TextField("Комментарий", null=True, blank=True)


class Message(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    text = models.TextField("Текст сообщения")
    house = models.ForeignKey(House, on_delete=models.SET_NULL, verbose_name='ЖК', null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, verbose_name='Секция', null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, verbose_name='Этаж', null=True, blank=True)
    flat = models.ForeignKey(Flat, on_delete=models.SET_NULL, verbose_name='Квартира', null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, verbose_name='Владелец квартир', null=True, blank=True)
    has_debt = models.BooleanField("Владельцам с задолженностями", default=False)
    created = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def recipients(self):
        answer = ''
        if self.owner is not None:
            return self.owner.fullname()
        if self.house is None:
            return 'Всем'
        answer = self.house.name
        if self.section is not None:
            answer += ', ' + self.section.name
        if self.level is not None:
            answer += ', ' + self.level.name
        if self.flat is not None:
            answer += ', кв.' + self.flat.number
        return answer
