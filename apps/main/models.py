from django.db import models
from tinymce.models import HTMLField

from apps.catalog.models import Product
from apps.main.mixins import MetaTagMixin


class Page(MetaTagMixin):
    name = models.CharField(verbose_name='Имя', max_length=255)
    slug = models.SlugField(unique=True)
    text = HTMLField(verbose_name='Содержание', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Информационная страница'
        verbose_name_plural = 'Информационные страницы'


class ProductSet(models.Model):
    products = models.ManyToManyField(Product, verbose_name='Товары')
    name = models.CharField(verbose_name='Название', max_length=255)
    sort = models.PositiveIntegerField(verbose_name='Сортировка', default=0)
    is_active = models.BooleanField(verbose_name='Активировано', default=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['sort']
        verbose_name = 'Карусель товара'
        verbose_name_plural = 'Карусель товаров'

