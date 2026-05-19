from django.db import models

class Domain(models.Model):
    name = models.CharField(max_length=200)
    weightage = models.IntegerField(help_text="Weightage in percentage")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.weightage}%)"

class Topic(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title
