from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fields = [
        'email',
        'user_id', 
        'nickname', 
        'name', 
        'university', 
        'admission_year', 
        'is_active',
        'profile_image',
        ]

    list_display = ['id'] + fields + ['date_joined']

admin.site.register(User, UserAdmin)