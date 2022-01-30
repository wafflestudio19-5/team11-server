from django.contrib import admin
from .models import EmailCode

# Register your models here.
class EmailCodeAdmin(admin.ModelAdmin):
    fields = [
        'email',
        'code',
        ]
    list_display = [
        'id',
        'email',
        'code',
        'updated_at'
        ]

admin.site.register(EmailCode, EmailCodeAdmin)