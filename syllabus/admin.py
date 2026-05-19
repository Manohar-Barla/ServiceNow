from django.contrib import admin
from .models import Domain, Topic

class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'weightage', 'description_short')
    search_fields = ('name', 'description')
    inlines = [TopicInline]

    def description_short(self, obj):
        return obj.description[:100]
    description_short.short_description = 'Description'

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'domain')
    list_filter = ('domain',)
    search_fields = ('title', 'content')
