from django.contrib import admin

from .models import User

# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_superuser']
    list_filter = ['username', 'is_staff', 'is_active']
