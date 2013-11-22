# Generate a random password 
import random

random.seed()
string = ""
for i in range(1000):
	bins = [random.randint(65, 90), random.randint(97, 122), random.randint(35,38), random.randint(48, 57)]
	whichbin = random.randint(0, 100)
	if whichbin < 80:
		char = random.choice(bins[0:2])
	else:
		char = random.choice(bins[2:4])	
	string = string + chr(char)
print string
