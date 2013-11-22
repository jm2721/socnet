from django.db import models
from users.models import WallPost, User

# Create your models here.

'''
    Like model. Can be bound to wallpost only, for now.
'''
class Like(models.Model):
    linked_to = models.ForeignKey(WallPost)
    liked_by = models.ForeignKey(User)

    def __str__(self):
        return str(self.liked_by) + " likes " + str(self.linked_to)

    class Meta:
        unique_together = ('linked_to', 'liked_by',)