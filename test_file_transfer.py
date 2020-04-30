import sys
from file_transfer import transfer_file

run_name = sys.argv[1]
        
files = ["random_text_100.txt", "random_text_1000.txt", "random_text_10000.txt"]
# files = ["random_text_1000000.txt"]
results_file = "file_transfer_results.csv"
for file in files:
	print("Testing file:", file, "for run on: ", run_name)
	duration, file_size = transfer_file("client", file)
	with open(results_file, "a") as f:
		row = file + "," + str(run_name) + "," + str(duration) + "," + str(file_size) + "\n"
		f.write(row)