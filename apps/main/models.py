from django.db import models
from tinymce.models import HTMLField
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
