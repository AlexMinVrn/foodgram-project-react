from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширенная модель для пользователей."""
    email = models.EmailField('Почта', max_length=254, unique=True)
    username = models.SlugField('Логин', max_length=150, unique=True,)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    is_subscribed = models.ManyToManyField(
        'User',
        through='Subscription',
        related_name='subscriptions',
        verbose_name='Подписки',
        blank=True
    )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    """Модель подписок"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписан'
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                name='unique_subscription',
                fields=['user', 'following'],
            ),
        ]

    def __str__(self):
        return f'{self.user} подписан  на {self.following}'
