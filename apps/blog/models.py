from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFill
from django.utils.safestring import mark_safe

from apps.main.mixins import MetaTagMixin
from apps.user.models import User
from config.settings import MEDIA_ROOT

class BlogCategory(MetaTagMixin):
    name = models.CharField(verbose_name='Имя категории', max_length=255)
    # image = models.ImageField(verbose_name='Изображение', upload_to='blog/category/', null=True)
    image = ProcessedImageField(
        verbose_name='Изображение',
        upload_to='blog/category/',
        processors=[ResizeToFill(600,400)],
        null=True,
        blank=True
    )


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория блога'
        verbose_name_plural = 'Категории блога'

    def image_tag_thumbnail(self):
        if self.image:
            return mark_safe(f"<img src='/{MEDIA_ROOT}{self.image}' width='70'>")

    image_tag_thumbnail.short_description = 'Изображение'

    def image_tag(self):
        if self.image:
            return mark_safe(f"<img src='/{MEDIA_ROOT}{self.image}'>")

    image_tag.short_description = 'Изображение'


class Tag(MetaTagMixin):
    name = models.CharField(verbose_name='Тэг', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг статьи'
        verbose_name_plural = 'Тэги статьи'


class Article(MetaTagMixin):
    category = models.ForeignKey(to=BlogCategory,verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок', max_length=225)
    text_preview = models.TextField(verbose_name='Текст-превью', null=True, blank=True)
    text = models.TextField(verbose_name='Текст')
    publish_date = models.DateTimeField(verbose_name='Дата публикации')
    tags = models.ManyToManyField(to=Tag, verbose_name='Тэги', blank=True)
    user = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_NULL, null=True, blank=True)
    image = ProcessedImageField(
        verbose_name='Изображение',
        upload_to='blog/article/',
        null=True,
        blank=True
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(600,400)]
    )
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def get_meta_title(self):
        if self.meta_title:
            return self.meta_title
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comments(models.Model):
    user = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(verbose_name="Название комментария", null=True, blank=True, max_length=255)
    username = models.CharField(verbose_name='Ваше имя', max_length=255, null=True, blank=True)
    email = models.EmailField(verbose_name='Ваш E-mail', null=True, blank=True)
    text = models.TextField(verbose_name='Текст вашего комментария', null=True, blank=True)
    article = models.ForeignKey(to=Article, verbose_name='Статья', on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name='Активировано', default=True)
    is_checked = models.BooleanField(verbose_name='Проверен', default=False)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'






