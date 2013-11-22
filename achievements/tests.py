"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from achievements.models import Achievement
from achievements.criteria import check_achievements, get_achievement
from achievements.populater import create_achievements
from users.models import User, WallPost
from datetime import datetime
from django.utils.timezone import utc

class TestAchievement(TestCase):
    
    def test_created_successfully(self):
        Achievement.objects.create(title="Testsuccessful", description="Test")
        self.assertTrue(Achievement.objects.filter(description="Test").exists())

    def test_check_achievements_friends(self):
        create_achievements()
        user = User.objects.create_user(username='test')
        
        check_achievements(user.id)
        self.assertFalse(user.has_achievement(get_achievement("Friendly")))
        self.assertFalse(user.has_achievement(get_achievement("Super Friendly")))
        self.assertFalse(user.has_achievement(get_achievement("Politician")))

        for i in range(1, 51):
            temp = User.objects.create_user(username=str(i))
            user.friends.add(temp)

        check_achievements(user.id)
        self.assertTrue(user.has_achievement(get_achievement("Friendly")))
        self.assertFalse(user.has_achievement(get_achievement("Super Friendly")))
        self.assertFalse(user.has_achievement(get_achievement("Politician")))
        
        for i in range(1, 51):
            temp = User.objects.create_user(username=str(i*100))
            user.friends.add(temp)

        check_achievements(user.id)
        self.assertTrue(user.has_achievement(get_achievement("Friendly")))
        self.assertTrue(user.has_achievement(get_achievement("Super Friendly")))
        self.assertFalse(user.has_achievement(get_achievement("Politician")))

        for i in range(1, 500):
            temp = User.objects.create_user(username=str(i*10000))
            user.friends.add(temp)

        check_achievements(user.id)
        self.assertTrue(user.has_achievement(get_achievement("Politician")))
        self.assertTrue(user.has_achievement(get_achievement("Super Friendly")))
        self.assertTrue(user.has_achievement(get_achievement("Politician")))

    def test_check_achievements_wallposts(self):
        create_achievements()
        now = datetime.utcnow().replace(tzinfo=utc)

        user = User.objects.create_user(username='test')
        other = User.objects.create_user(username='other')
        user.friends.add(other)
        self.assertFalse(user.has_achievement(get_achievement("Outspoken")))
        self.assertFalse(user.has_achievement(get_achievement("Social climber")))

        for i in range(1, 51):
            WallPost.objects.create(message="bla", pub_date=now, poster=user, receiver=other)

        check_achievements(user.id)
        self.assertTrue(user.has_achievement(get_achievement("Outspoken")))
        self.assertFalse(user.has_achievement(get_achievement("Social climber")))

        for i in range(1, 151):
            WallPost.objects.create(message="bla", pub_date=now, poster=user, receiver=other)

        check_achievements(user.id)
        self.assertTrue(user.has_achievement(get_achievement("Outspoken")))
        self.assertTrue(user.has_achievement(get_achievement("Social climber")))