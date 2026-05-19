from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'question_number', 'question_type', 'topic', 'question_text',
            'option_a', 'option_b', 'option_c', 'option_d', 'option_e',
            'correct_answers', 'explanation', 'question_image'
        ]
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 4}),
            'explanation': forms.Textarea(attrs={'rows': 3}),
        }

class BulkUploadForm(forms.Form):
    file = forms.FileField(
        label='Select a TXT, PDF, or DOCX file',
        help_text='Make sure the file follows the specified question format.'
    )
