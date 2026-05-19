from django.contrib import admin
from .models import Resource
import os

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'file_size')
    search_fields = ('title', 'description')
    readonly_fields = ('uploaded_at',)

    def file_size(self, obj):
        try:
            size = obj.file.size
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.2f} KB"
            else:
                return f"{size / (1024 * 1024):.2f} MB"
        except:
            return "N/A"
    file_size.short_description = 'Size'
