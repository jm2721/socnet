from django.db import models
from django.conf import settings

# Create your models here.

class PrivateMessage(models.Model):
    message = models.TextField(max_length=3000)
    send_date = models.DateTimeField('Date Sent')
    # The following two fields have to have 'related_name' as pm-(sender or reciver) because
    # otherwise they conflict with the senders and receivers for wallposts
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='pmsender', null=False)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='pmreceiver', null=False) 
