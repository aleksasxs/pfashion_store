# Generated by Django 4.1.3 on 2022-11-17 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_article_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Тэг')),
                ('tags', models.ManyToManyField(to='blog.article')),
            ],
            options={
                'verbose_name': 'Тэг статьи',
                'verbose_name_plural': 'Тэги статьи',
            },
        ),
    ]
