from django.contrib import admin

from .models import Cookbook


@admin.register(Cookbook)
class CookbookAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'created_at']
    filter_horizontal = ['recipes']
