import random, sys
from users.models import User, WallPost
#from django.conf import settings as settings_conf
#from django.core.management import setup_environ
#from socnet import settings
from django.utils import timezone
from optparse import OptionParser
import hashlib
import sys, os

print "There are " + str(len(User.objects.all())) + " users in the database"
show = raw_input("Print them? y/n ")
if show == 'y':
    for u in User.objects.all():
        print u
print "There are " + str(len(WallPost.objects.all())) + " wallposts in db"
