from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    """Модель категорий"""
    name = models.CharField('Имя', max_length=100)
    slug = models.SlugField(max_length=128)
    description = models.TextField('Описание', max_length=1000, default='', blank=True)

    parent = TreeForeignKey(
        'self',
        verbose_name='Родительская категория',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    template = models.CharField('Шаблон', max_length=500, default='blog/post_list.html')
    published = models.BooleanField('Опубликованно', default=True)
    paginated = models.PositiveIntegerField('Количество постов на странице', default=5)
    sort = models.PositiveIntegerField('Порядок', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField('Имя', max_length=100)
    slug = models.SlugField(max_length=128)
    published = models.BooleanField('Отображать', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Post(models.Model):
    """Модель постов"""
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    title = models.CharField('Заголовок', max_length=300)
    subtitle = models.CharField('Подзаголовок', max_length=300, blank=True, null=True)
    mini_text = models.TextField('Краткое содержание контента', max_length=5000)
    text = models.TextField('Контент', max_length=10000000)
    slug = models.SlugField()

    image = models.ImageField('Главная фотография', upload_to='post/', null=True, blank=True)

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        blank=True
    )

    created_date = models.DateTimeField('Дата создания', auto_now_add=True)
    published_date = models.DateTimeField(
        'Дата публикации',
        default=timezone.now,
        blank=True,
        null=True
    )
    edit_date = models.DateTimeField(
        'Дата редактирования',
        default=timezone.now,
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        null=True
    )

    template = models.CharField('Шаблон', max_length=500, default='blog/post_detail.html')
    published = models.BooleanField('Опубликованно', default=True)
    viewed = models.PositiveIntegerField('Просмотров', default=0)
    status = models.BooleanField('Для зарегистрированных', default=False)
    sort = models.PositiveIntegerField('Порядок', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    """Модель комментариев"""
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    text = models.TextField('Текст')
    created_date = models.DateTimeField('Дата создания', auto_now_add=True)
    moderation = models.BooleanField('Модерирован')

    post = models.ForeignKey(
        Post,
        verbose_name='Пост',
        on_delete=models.CASCADE
    )
