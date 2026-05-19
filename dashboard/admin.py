from django.contrib import admin
from .models import TestAttempt

@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'percentage', 'score', 'total_questions', 'date')
    list_filter = ('user', 'date')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('date',)

    def has_add_permission(self, request):
        return False # Attempts should only be created via the test engine
