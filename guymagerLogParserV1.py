import os
import subprocess
import sys
import re

# set input variables for the source and destination file directories

source_dirname= str(sys.argv[1])
dest_dir = str(sys.argv[2])



files = []


for file in os.listdir(source_dirname):
	if file.endswith(".info"):
		files.append(source_dirname + "\\" + file)

outfile = open(dest_dir + "ParsedLog.csv", 'w')		

outfile.write("Barcode,FilePath,Format,Number of Bytes,Time taken,MD5 Hash,Bad sectors\n")

for filename in files:

	
	barcode, format, filepath, numBytes, timeTaken, MD5Hash = "","","","","",""
	for line in open(filename):	
		
	
		
		if line.startswith('   Case number'):
			res = re.search(":\s\d+",line)
			barcode = res.group(0)[2:].replace(",","")
			
		if line.startswith('Image path and file name'):
			#print line
			res = re.search(":\s.+",line)
			if res is None:
				throw = ""
			else:
				filepath = res.group(0)[2:].replace(",","")
			#print filepath
			#print res.group(0)
		
		if line.startswith('   User Capacity:'):
			res = re.search("\s\d.+bytes",line)
			numBytes = res.group(0)[:-5].replace(",","")
			
			
		if line.startswith('Ended'):
			res = re.search("\(.+\)",line)
			timeTaken = res.group(0)[1:-1].replace(",","")
			
		if line.startswith('MD5 hash                   :'):
			res = re.search(":.+",line)
			MD5Hash = res.group(0)[2:].replace(",","")
			
		if line.startswith('Format   '):
			res = re.search(":.+",line)
			format = res.group(0)[2:-25].replace(",","")	
		if line.startswith('State: '):
			#print line
			res = re.search(":.+",line)
			errors = res.group(0)[30:-12].replace(",","")	
			#print errors
			
	outfile.write(barcode + "," + filepath + "," + format + "," + numBytes + "," + timeTaken + "," + MD5Hash + "," + errors + "\n")


outfile.close()
