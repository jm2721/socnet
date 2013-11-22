"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib import auth
from django.test import TestCase
from users.models import User, WallPost, Request
from likes.models import Like
from django.utils import timezone


class TestUsers(TestCase):
    def test_users_created(self):
        sample_user = User.objects.create_user(username='j', password='j')
        self.assertEquals(User.objects.filter(username='j').exists(), True)

    def test_relations(self):
        friend = User.objects.create_user(username='friend', password='friend')
        other_friend = User.objects.create_user(username='other_friend', password='other_friend')

        friend.friends.add(other_friend)

        self.assertEquals('other_friend' in friend.friend_usernames(), True)
        self.assertEquals('friend' in other_friend.friend_usernames(), True)

class TestWallPosts(TestCase):

    def test_wallpost_created(self):
        user1 = User.objects.create_user(username='blabla', password='blabla')
        user2 = User.objects.create_user(username='b', password='b')
        user1.friends.add(user2)
        wp = WallPost.objects.create(message='blablabal', poster=user1, receiver=user2, pub_date=timezone.now())

        self.assertEquals(WallPost.objects.filter(message='blablabal').exists(), True)
        self.assertEquals(WallPost.objects.filter(message='blablabal')[0].poster.username == 'blabla', True)
        self.assertEquals(WallPost.objects.filter(message='blablabal')[0].receiver.username == 'b', True)

    def test_user_can_only_post_to_friend(self):
        user1 = User.objects.create_user(username='blabla', password='blabla')
        user2 = User.objects.create_user(username='b', password='b')

        self.assertRaises(ValidationError, lambda: WallPost.objects.create(message='something', pub_date=timezone.now(), poster=user1, receiver=user2))
        self.assertEqual(WallPost.objects.filter(message='something').exists(), False)

class TestRequests(TestCase):

    def test_request_created(self):
        user1 = User.objects.create_user(username='blabla', password='blabla')
        user2 = User.objects.create_user(username='b', password='b')
        req = Request.objects.create(requester=user1, requestee=user2)
        self.assertEquals(Request.objects.filter(requester=user1, requestee=user2).exists(), True)

    def test_request_error_if_already_friend(self):
        user1 = User.objects.create_user(username='blabla', password='blabla')
        user2 = User.objects.create_user(username='b', password='b')
        user1.friends.add(user2)

        self.assertRaises(ValidationError, lambda: Request.objects.create(requester=user1, requestee=user2))
