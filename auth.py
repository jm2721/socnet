import hashlib
import sys


def generate_user_pass_pairs(num_of_users):
	p = open('.p', 'w')
	for u in range(num_of_users):
		usr = hashlib.sha512()
		usr.update(str(u+1))
		pswd = hashlib.sha512()
		pswd.update(str(u+1))
		p.write(usr.hexdigest())
		p.write(pswd.hexdigest())
	p.close()

def check_validity(u_num):	
	tries = 5
	while tries > 0:
		pswd_raw = raw_input("What is the password? ")
		pswd = hashlib.sha512()
		pswd.update(str(pswd_raw)) 

		with open(".p", 'r') as p:
			p.seek((int(u_num)*256)-128, 0)
			check = p.read(128)
			if pswd.hexdigest() == check:
				print "Correct"
				sys.exit()
			else:
				print "Incorrect password. Please try again"
				tries -= 1
	print "Login failed. Try again never"
