from django.contrib import admin
from apps.main.models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass


