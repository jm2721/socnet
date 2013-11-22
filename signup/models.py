from django.db import models

# Create your models here.

class ConfirmationCode(models.Model):
    code = models.CharField(max_length=128, default='')
    uid = models.CharField(max_length=128, default='')

    class Meta:
        unique_together = ('code', 'uid',)
