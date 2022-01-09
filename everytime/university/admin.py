from django.contrib import admin
from .models import University

# Register your models here.
class UniversityAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'email_domain', 
        ]
    list_display = ['id'] + fields

admin.site.register(University, UniversityAdmin)