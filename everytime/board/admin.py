from django.contrib import admin
from .models import Board

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'manager',
        'description',
        ]
    list_display = [
        'id',
        'name',
        'university',
        'manager',
        'type',
        'description',
        'allow_anonymous',
        ]

admin.site.register(Board, BoardAdmin)