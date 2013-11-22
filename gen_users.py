def readfile(filepath, mode='r'):
	with open(filepath, mode) as infile:
		for line in infile:
			yield infile.readline()


def generate_random_user(verbose=False):
    first_names = readfile("fnames.txt", 'r')
    last_names = readfile("lnames.txt", 'r')

    fname = first_names.next().split()[0].lower()
    lname = last_names.next().split()[0].lower()
	username = user = '{fname}{lname}'.format(fname=fname.lower(), lname=lname)
	email = '{username}@sample.com'.format(username=username)
	first_name = fname.title()
	last_name = lname.title()

    if verbose:
        print "Generated user: %s %s" % (first_name, last_name)
    
	user, is_new = User.objects.get_or_create(username=username, defaults={
																first_name: first_name,
																last_name: last_name,
																email: email,
																username: username,
																password: first_name.lower()
																}
	
    if not is_new:
        user = User.objects.create_user(first_name=first_name,
										last_name=last_name,
										email=email,
										username=str(random.randint(1, 10000))  # Esto revisalo porque no va,
										password=first_name.lower())


