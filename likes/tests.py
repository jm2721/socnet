"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from likes.models import Like
from users.models import User, WallPost
from django.utils.timezone import utc
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class LikeTest(TestCase):
    def test_created_correctly(self):
        self.now = datetime.utcnow().replace(tzinfo=utc)
        self.user = User.objects.create(username='test')
        self.other = User.objects.create(username='other')
        self.user.friends.add(self.other)
        self.wallpost = WallPost.objects.create(message='test', poster=self.user, receiver=self.other, pub_date=self.now)
        
        self.like = Like.objects.create(linked_to=self.wallpost, liked_by=self.user)
        
        # Test created
        self.assertTrue(Like.objects.filter(linked_to=self.wallpost, liked_by=self.user).exists())

        # Test not unique separately. User is the same but wallpost is different.
        self.otherpost = WallPost.objects.create(message='some other wall post', poster=self.user, receiver=self.other, pub_date=self.now)
        self.like2 = Like.objects.create(linked_to=self.otherpost, liked_by=self.user)
        self.assertTrue(Like.objects.filter(linked_to=self.otherpost, liked_by=self.user).exists())

        # Test not unique separately, User is different but wallpost is same.
        self.like3 = Like.objects.create(linked_to=self.otherpost, liked_by=self.other)
        self.assertTrue(Like.objects.filter(linked_to=self.otherpost, liked_by=self.other).exists())

        # Test unique together. I need to run this last because after the create() command runs all database
        # transactions are aborted until the next rollback because create() raises an error.
        self.assertRaises(IntegrityError, lambda: Like.objects.create(linked_to=self.wallpost, liked_by=self.user))

