from django.db import models

class BlogCategory(models.Model):
    name = models.CharField(verbose_name = 'Имя категории', max_length = 255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория блога'
        verbose_name_plural = 'Категории блога'

class Article(models.Model):
    category = models.ForeignKey(to=BlogCategory,verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок', max_length=225)
    text_preview = models.TextField(verbose_name='Текст-превью', null=True, blank=True)
    text = models.TextField(verbose_name='Текст')
    publish_date = models.DateTimeField(verbose_name='Дата публикации')
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class Tag(models.Model):
    name = models.CharField(verbose_name = 'Тэг', max_length = 255)
    tags = models.ManyToManyField(Article)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг статьи'
        verbose_name_plural = 'Тэги статьи'