# WARNING: RUN THIS SCRIPT IN SAME DIRECTORY AS DATABASE OTHERWISE THE DATABASE WILL GET WIPED OUT
import random, sys
from users.models import User, WallPost, Request
from django.utils import timezone
from optparse import OptionParser
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import hashlib
import sys, os

def generate_random_user(fnames, lnames, verbose=False):
    for line in first_names:
        fnames.append(line.split()[0].lower())

    for line in last_names:
        lnames.append(line.split()[0].lower())
        
    first_name = fnames[random.randint(0, len(fnames)-1)]
    last_name = lnames[random.randint(0, len(lnames)-1)]
    first_char = first_name[0]
    last_char = last_name[0]
    email = first_name + last_name + "@sample.com"
    username = first_name + last_name
    
    first = first_char.upper() + first_name[1:]
    last = last_char.upper() + last_name[1:]
    
    if verbose:
        print "Generated user: %s %s" % (first, last)
    '''user, is_new = User.objects.get_or_create(username=username, defaults={
                                                                'first_name': first,
                                                                'last_name': last,
                                                                'email': email,
                                                                'username': username,
                                                                'password': first_name.lower()
                                                                })'''
    if not User.objects.filter(username=username):
        User.objects.create_user(username=username, 
                                 first_name=first, 
                                 last_name=last, 
                                 email=email, 
                                 password=first_name.lower())
    else:
        print "Found duplicate name. Username modified"
        user = User.objects.create_user(first_name=first,
                                        last_name=last,
                                        email=email,
                                        # If this username has already been taken, 
                                        # append the length of the queryset where username=username. 
                                        # This number will never be the same between two users with 
                                        # same first and last names because the length of the queryset 
                                        # increases each time
                                        username=username + str(len(User.objects.filter(username__icontains=username))),
                                        password=first_name.lower())
 
    '''if not is_new:
        print "Found duplicate name. Username modified"
        user = User.objects.create_user(first_name=first,
                                        last_name=last,
                                        email=email,
                                        # If this username has already been taken, append the length of the queryset where username=username. This number will never be the same between two users with same first and last names because the length of the queryset increases each time
                                        username=username + str(len(User.objects.filter(username__icontains=username))),
                                        password=first_name.lower())'''
 
# Not really necessary anymore. Function from a bygone age
def test_uids():
    uids = []
    for u in User.objects.all():
        uids.append(u.id)

    for i in range(1, len(uids)-1):
        if uids[i] != uids[i-1]+1:
            print str(uids[i]) + " skipped one"
            print "Patching..."
            User.objects.create_user(username="patchusername" + str(random.randint(1, 100000)), first_name="user"+str(random.randint(1, 100000)), last_name="last", email="sample@sample.com", password="patch", id=uids[i]-1)
            return test_uids()
    print "Done"
    return True

# Not needed anymore.                    
def generate_user_pass_pairs(user_id, new_password, p, salt=None):
    usr = hashlib.sha512()
    usr.update(str(user_id))
    pswd = hashlib.sha512()
    pswd.update(str(new_password) + str(salt))
    p.write(usr.hexdigest())
    p.write(pswd.hexdigest())

'''def update_password(u_id, new_pass):
    p = open('.p', 'w')
    p.seek((int(u_id)*256)-128, 0)
    p.write("")
    p.close()
    p = open('.p', 'a')
    pswd = hashlib.sha512()
    pswd.update(str(new_password))
    p.write(pswd.hexdigest())
    p.close()'''

def return_first_repeated():
    for u in User.objects.all():
        if u.username[len(u.username)-1] == '1':
            print u.id
            print u.username
            return u.id

def generate_relations(friends_per_person, show_relations=False):
    random.seed()
    # For this to work they need to be ordered by id
    first_id = User.objects.all()[0].id 
    last_id = first_id + (len(User.objects.all())-1)
    for u in User.objects.all():
        for i in range(friends_per_person):
            friend_to_add = User.objects.get(id=random.randint(first_id, last_id-1))
            u.friends.add(friend_to_add)
            if show_relations:
                print "Added a relation between " + str(u) + " and " + str(friend_to_add)

def check_exists(u_num):
    if u_num > len(User.objects.all()):
        return False
    else:
        return True

def check_validity(u_num, given_pass=False, given_pswd=None):
    if not check_exists(u_num):
        print "User doesn't exist"
        return False

    if not given_pass:
        pswd_raw = raw_input("What is the password? ")
    else:
        pswd_raw = given_pswd
    salt = User.objects.get(pk=u_num).salt
    pswd = hashlib.sha512()
    pswd.update(str(pswd_raw) + str(salt))

    with open(".p", 'r') as p:
        p.seek((int(u_num)*256)-128, 0)
        check = p.read(128)
        print check
        print pswd.hexdigest()
        if pswd.hexdigest() == check:
            return True
        else:
            return False

def generate_requests(requests):
    first_id = User.objects.all()[0].id 
    last_id = first_id + (len(User.objects.all())-1)

    for r in range(requests):
        try:
            # Uncomment following line to create a lot of requests for a particular user. Useful for debugging.
            #Request.objects.create(requester=User.objects.get(id=random.randint(first_id, last_id)), requestee=User.objects.get(username='j'))
            Request.objects.create(requester=User.objects.get(id=random.randint(first_id, last_id)), requestee=User.objects.get(id=random.randint(first_id, last_id)))
        except ValidationError:
            pass

def generate_wall_posts(wall_posts_per_person, filler, verbose):
    # For this to work they need to be ordered by id
    first_id = User.objects.all()[0].id 
    last_id = first_id + (len(User.objects.all())-1)
    for u in User.objects.all():
        friend_ids = [f.id for f in u.friends.all()]
        for i in range(wall_posts_per_person):
            msg = filler.read(random.randint(5, 300))
            filler.seek(0, 0)
            published_on = timezone.now()
            poster = u.friends.get(id=friend_ids[random.randint(0, len(friend_ids)-1)])
            post = WallPost.objects.create(message=msg, 
                                            pub_date=published_on, 
                                            poster=poster,
                                            receiver=u)
            if verbose:
                print str(post.poster) + " posted a message on " + str(u) + "'s wall"

def delete_all_friends():
    for u in User.objects.all():
        for f in u.friends.all():
            u.friends.remove(f)
if __name__ == "__main__":
    parser = OptionParser()         

    parser.add_option("-u", "--users",
            action="store", type="int", dest="users_to_add", help="Specify how many users to create")

    parser.add_option("-r", "--relations",
            action="store", type="int", dest="relations", help="Specify how many relations to create between users")
    
    parser.add_option("-q", "--requests",
            action="store", type="int", dest="requests", help="Specify how many friend requests to create")

    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="Show all the actions that are being carried out")

    parser.add_option("-w", "--wall_posts",
            action="store", type="int", dest="wall_posts", help="Specify the number of wall posts to create per person")

    parser.add_option("-i", "--initial-upswds", action="store_true", dest="init_upswds", help="Generate the user passwords for the first time")
    
    parser.add_option("--clear-all", action="store_true", dest="clear_everything", help="Clear all wall posts, users, and passwords")

    parser.add_option("-c", "--crack",
        action="store", type="int", dest="crack_id", help="Find out a users password")

    parser.add_option("--isword", action="store_true", dest="isword", help="Indicate that the password to crack is a combination of only letters")
    
    parser.add_option("--patch", action="store_true", dest="patch", help="Path the database so that all the user ids are in order and there are no gaps.")
    
    (options, args) = parser.parse_args()
    verbose = options.verbose


    if options.patch:
        test_uids()
        
    if options.requests:
        generate_requests(options.requests)
        print "Created requests successfully"


    if options.init_upswds:
        p = open('.p', 'w')
        for u in User.objects.all():    
            generate_user_pass_pairs(u.id, u.id, p, u.salt)
            print u.salt
        p.close()

    if options.crack_id:
        crack(options.crack_id, options.isword)

    if options.clear_everything:
        check = raw_input("Are you really sure you would like to delete all the information in the table? This action is final. y/n ")
        if check == 'n':
            print "Closing program"
            sys.exit()
        elif check == 'y':
            print "Deleting users..."
            for u in User.objects.all():
                u.delete()  
            print "Deleting wall posts..."
            for w in WallPost.objects.all():
                w.delete()
            print "Removing .p file if exists"
            try:
                os.remove('.p')
            except:
                pass
            print "All done. Completed successfully"
            
    if options.users_to_add:
        first_names = open("fnames.txt", 'r')
        last_names = open("lnames.txt", 'r')
        random.seed()
        fnames = []
        lnames = []
        for line in first_names:
            fnames.append(line.split()[0].lower())

        for line in last_names:
            lnames.append(line.split()[0].lower())
    
        if len(User.objects.all()) == 0:
            User.objects.create_user(first_name = 'Juan', last_name = 'Marron', email = 'jm2721@trevor.org', username='j', password='j')
        for i in range(options.users_to_add):
            temp = generate_random_user(fnames, lnames, verbose)
        first_names.close()
        last_names.close()
        print "Created users successfully"

    if options.relations:
        generate_relations(options.relations, verbose)
        print "Generated relations successfully"
    
    if options.wall_posts:
        random.seed()
        filler = open('filler.txt', 'r')  
        generate_wall_posts(options.wall_posts, filler, verbose)
        filler.close()
        print "Generated wall posts successfully"
    
    if not options.wall_posts and not options.users_to_add and not options.relations and not options.requests:
        print "Type ./mngr.py --help for help"
