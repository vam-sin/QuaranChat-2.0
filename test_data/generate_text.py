import sys
import random

num_chars = int(sys.argv[1])
with open("random_text_"+str(num_chars)+".txt", "w") as f:
	while num_chars != 0:
		character = random.randint(65, 90)
		f.write(chr(character))
		num_chars -= 1
print("Successful")