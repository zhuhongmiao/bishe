from django.contrib import admin
from .models import Fabric
# Register your models here.

@admin.register(Fabric)
class FabricAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_name', 'price', 'like')
    search_fields = ('title', 'category_name', 'pattern')
    list_filter = ('category_name', 'country', 'pattern')
