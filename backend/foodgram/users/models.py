from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    '''Подписка на автора рецепта:
    author - Автор рецепта;
    user   - Подписчик на автора.
    '''
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='sub_author'
    )
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик на автора',
        on_delete=models.CASCADE,
        related_name='sub_user'
    )

    class Meta:
        ordering = ['user']
        verbose_name = 'Подписка на автора рецепта'
        verbose_name_plural = 'Подписки на автора рецепта'
        constraints = [
            models.UniqueConstraint(
                name="unique_subscriptions",
                fields=['author', 'user'],
            ),
        ]

    def __str__(self):
        return f'{self.user} {self.author}'
