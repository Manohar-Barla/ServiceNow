from django.db import models
from django.contrib.auth.models import User

class TestAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField()
    total_questions = models.IntegerField()
    percentage = models.FloatField()
    test_name = models.CharField(max_length=100, default='CSA Mock Exam')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.percentage}% on {self.date.strftime('%Y-%m-%d')}"
