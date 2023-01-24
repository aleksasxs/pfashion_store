from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.catalog.models import Product
from apps.main.mixins import MetaTagMixin
from apps.user.models import User


class Cart(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)
    total = models.DecimalField(verbose_name='Итого', max_digits=12, decimal_places=2)
    first_name = models.CharField(verbose_name='Имя', max_length=225)
    last_name = models.CharField(verbose_name='Фамилия', max_length=225)
    email = models.EmailField(verbose_name='E-mail')
    phone = PhoneNumberField(verbose_name='Телефон')
    address = models.TextField(verbose_name='Адрес')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'