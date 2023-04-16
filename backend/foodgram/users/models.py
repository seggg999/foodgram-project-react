from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True


class Subscription(models.Model):
    '''Подписка на автора рецепта:
    author - Автор рецепта;
    user   - Подписчик на автора.'''

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
        constraints = [
            models.UniqueConstraint(
                name="unique_subscriptions",
                fields=['author', 'user'],
            ),
        ]

    def __str__(self):
        return f'{self.user} {self.author}'
