from django.db import models
from syllabus.models import Domain

class Question(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    
    CORRECT_ANSWER_CHOICES = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
        ('4', 'Option 4'),
    ]
    correct_answer = models.CharField(max_length=1, choices=CORRECT_ANSWER_CHOICES)
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"{self.domain.name}: {self.question_text[:50]}..."
