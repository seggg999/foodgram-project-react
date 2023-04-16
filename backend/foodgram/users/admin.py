from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Subscription

User = get_user_model()


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'user',
    )
    search_fields = ('user',)
    list_filter = ('user',)


admin.site.register(Subscription, SubscriptionAdmin)
