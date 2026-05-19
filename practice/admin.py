from django.contrib import admin
from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text_short', 'domain', 'correct_answer')
    list_filter = ('domain', 'correct_answer')
    search_fields = ('question_text', 'explanation', 'option1', 'option2', 'option3', 'option4')
    list_per_page = 20

    def question_text_short(self, obj):
        return obj.question_text[:75]
    question_text_short.short_description = 'Question'
