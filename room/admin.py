from django.contrib import admin
from .models import Media
# Register your models here.

class MediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'select', 'price_str' , '']


admin.site.register(Media)