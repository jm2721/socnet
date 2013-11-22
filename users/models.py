from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from achievements.models import Achievement
import os
import hashlib

# Create your models here.

''' To Implement:
        Password Strength Checking
        Throttling of login attempts (retry wrapper)
        Authentication against third-parties (OAuth, for example)
    The above taken from the django website, they are the things django does not include in the auth system.

    Also, ImageField class on User so User can upload image.
'''
class User(AbstractUser):
    friends = models.ManyToManyField('self', null=True, blank=True)
    achievements = models.ManyToManyField(Achievement)
    
    def friend_names(self):
        return ', '.join([str(u) for u in self.friends.all()])
    friend_names.short_description = "Friends"

    def friend_usernames(self):
        return ', '.join([str(u.username) for u in self.friends.all()])
    friend_names.short_description = "Friend usernames"
    
    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    def has_achievement(self, achievement):
        return achievement in self.achievements.all() 

    def __str__(self):
        return self.get_full_name()

    class Meta:
        ordering = ['id']

class Request(models.Model):
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requester', null=False)
    requestee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requestee', null=False)

    def validate(self):

        from django.core.exceptions import ValidationError
        if self.requester in self.requestee.friends.all():
            raise ValidationError("Requester is already friends with this person")

    def save(self, *args, **kwargs):
        self.validate()
        super(Request, self).save(*args, **kwargs)

    def accept(self):
        self.requester.friends.add(self.requestee)
        self.requestee.friends.add(self.requester)
        self.delete()
    def decline(self):
        self.delete()

    def __str__(self):
        return str(self.requester) + " sent  " + str(self.requestee) + " a friend request"


class WallPost(models.Model):
    message = models.TextField(max_length=3000)
    pub_date = models.DateTimeField('Date Published')
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='poster', null=False)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver', null=False)
    
    def validate(self):
        from django.core.exceptions import ValidationError
        if self.poster.username not in self.receiver.friend_usernames() and self.poster != self.receiver:
            raise ValidationError("Poster must be a friend of receiver to be able to post.")
    def save(self, *args, **kwargs):
        self.validate()
        super(WallPost, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.poster) + " posted a message on " + str(self.receiver) + "'s wall"
