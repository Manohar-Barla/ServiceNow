from django.db import models

class Question(models.Model):
    TYPE_CHOICES = [
        ('SINGLE_CHOICE', 'Single Choice'),
        ('MULTIPLE_SELECT', 'Multiple Select'),
    ]

    TOPIC_CHOICES = [
        ('Automation', 'Automation'),
        ('Collaboration', 'Collaboration'),
        ('DB & Security', 'DB & Security'),
        ('Instance', 'Instance'),
        ('Integration', 'Integration'),
        ('Platform', 'Platform'),
    ]

    question_number = models.IntegerField(blank=True, null=True)
    question_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='SINGLE_CHOICE')
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)
    question_text = models.TextField()
    
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    option_e = models.CharField(max_length=500, blank=True, null=True)
    
    correct_answers = models.CharField(max_length=100, help_text="Comma-separated options, e.g., 'A,C,D'")
    question_image = models.ImageField(upload_to='questions/', blank=True, null=True)
    explanation = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} - Q{self.question_number or '?'}: {self.question_text[:50]}"

    class Meta:
        ordering = ['-created_at']
