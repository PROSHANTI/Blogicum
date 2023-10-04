from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from pages.models import PublishedModel

title_len = 20


class Category(PublishedModel):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
        blank=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; разрешены '
                   'символы латиницы, цифры, дефис и подчёркивание.'),
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title[:title_len]

    def get_absolute_url(self):
        return reverse('blog:category_posts',
                       kwargs={'category_slug': self.slug})


class Location(PublishedModel):
    name = models.CharField(
        max_length=256,
        verbose_name='Название места',
        blank=True,
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name[:title_len]


class Post(PublishedModel):
    User = get_user_model()
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
        blank=True,
    )
    text = models.TextField(
        verbose_name='Текст',
        blank=True,
    )
    pub_date = models.DateTimeField(
        blank=True,
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.'),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )

    image = models.ImageField(
        'Изображение',
        upload_to='post_images',
        blank=True,
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.title[:title_len]

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    User = get_user_model()
    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='Пост',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'сomments'

    def __str__(self) -> str:
        return (f'Комментарий "{self.text}" от пользователя "{self.author}" '
                f'к посту "{self.post}"')
