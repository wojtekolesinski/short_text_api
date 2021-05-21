from django.contrib import admin
from .models import ShortText


@admin.register(ShortText)
class ShortTextAdmin(admin.ModelAdmin):
    fields = ['title', 'text', 'viewcount']
