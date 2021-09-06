from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from admin.singleton import SingletonModel


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
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)


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


class Service(models.Model):
    """Модель хранит коммунальные услуги"""

    name = models.CharField("Услуга", max_length=50)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    show = models.BooleanField("Показывать в счетчиках")

    def __str__(self):
        return self.name
