import random, sys
from users.models import User, WallPost

print "Users in database: " + str(len(User.objects.all()))

rels = 0
for u in User.objects.all():
	for f in u.friends.all():
		rels += 1
average = rels/len(User.objects.all())

print "Number of friendships: " + str(rels)
print "Average number of friends per person: " + str(average)
	
print "Number of WallPosts: " + str(len(WallPost.objects.all()))

