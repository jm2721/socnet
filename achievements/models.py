from django.db import models

# Create your models here.

class Achievement(models.Model):
    title = models.CharField(max_length=50, default='ach title', unique=True)
    # Description shouldn't be too long, something like "Reached 50 friends"
    description = models.CharField(max_length=300, null=False)

    def __str__(self):
        return self.title + ": " + self.description
