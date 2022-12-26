from django.contrib import admin

from .models import User, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username')
    list_filter = ('email', 'username')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    list_filter = ('user', 'following')
