from django.contrib import admin
from .models import ShortText
from django.contrib.auth.models import User

# Register your models here.


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     fields = ['username', 'email', 'first_name', 'last_name']


@admin.register(ShortText)
class ShortTextAdmin(admin.ModelAdmin):
    fields = ['title', 'text', 'viewcount']
