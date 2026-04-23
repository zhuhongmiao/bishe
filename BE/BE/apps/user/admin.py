from django.contrib import admin
from .models import User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_admin')
    search_fields = ('username',)
    list_filter = ('is_admin',)
