from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from .helpers import truncate_string

User = get_user_model()

TEXT_LENGTH = 256
TITLE_LENGTH = 20


class BlogBaseModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Post(BlogBaseModel):
    title = models.CharField(
        max_length=TEXT_LENGTH,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время '
            'в будущем — можно делать отложенные публикации.'
        )
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    image = models.ImageField(
        upload_to='post_images',
        blank=True, null=True,
        verbose_name='Изображение',
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'png', 'gif'])]
    )

    class Meta:
        default_related_name = 'post'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return truncate_string(self.title, TITLE_LENGTH)


class Category(BlogBaseModel):
    title = models.CharField(max_length=TEXT_LENGTH, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        max_length=64,
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return truncate_string(self.title, TITLE_LENGTH)


class Location(BlogBaseModel):
    name = models.CharField(
        max_length=TEXT_LENGTH,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return truncate_string(self.name, TITLE_LENGTH)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name='Публикация')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Опубликовано')

    class Meta:
        default_related_name = 'comments'
        ordering = ['created_at']
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий {self.author}'
