from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Subscription

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'password',
        'first_name',
        'last_name',
    )
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'user',
    )
    search_fields = ('user', 'author')
    list_filter = ('user',)
    empty_value_display = '-пусто-'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
