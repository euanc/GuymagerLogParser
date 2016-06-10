import os
import sys
import re
import argparse
import csv
from glob import glob

# set input variables for the source and destination file directories
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputdir', metavar='[input_dir]',
                        help='input directory with .info files')
    parser.add_argument('outputfile', metavar='[output_file]',
                        help='output file for CSV data')
    args = parser.parse_args()

    # Does output dir exist?
    try:
        os.path.exists(args.inputdir)
    except:
        sys.exit('Quitting: Input directory does not exist.')

    # Does output file exist?
    if os.path.isfile(args.outputfile):
        sys.exit('Output file already exists; will not overwrite.')

    # Set up output file
    outfile = open(args.outputfile, 'w')
    fieldnames = ['Barcode','FilePath','Format','Number of Bytes','Time taken','MD5 Hash','Bad sectors']
    outfilecsv = csv.DictWriter(outfile, fieldnames=fieldnames)
    outfilecsv.writeheader()

    files = glob(os.path.join(args.inputdir, '*.info'))

    for filename in files:
        parsedline = {}
        for line in open(filename, 'rU'): 
            
            if line.startswith('   Case number'):
                res = re.search(":\s\d+",line)
                if res is not None:
                    parsedline['Barcode'] = res.group(0)[2:].replace(",","")
                else:
                    parsedline['Barcode'] = ''
                
            if line.startswith('Image path and file name'):
                #print line
                res = re.search(":\s.+",line)
                if res is None:
                    throw = ""
                else:
                    parsedline['FilePath'] = res.group(0)[2:].replace(",","")
            
            if line.startswith('   User Capacity:'):
                res = re.search("\s\d.+bytes",line)
                parsedline['Number of Bytes'] = res.group(0)[:-5].replace(",","")
                
            if line.startswith('Ended'):
                res = re.search("\(.+\)",line)
                parsedline['Time taken'] = res.group(0)[1:-1].replace(",","")
                
            if line.startswith('MD5 hash                   :'):
                res = re.search(":.+",line)
                parsedline['MD5 Hash'] = res.group(0)[2:].replace(",","")
                
            if line.startswith('Format   '):
                res = re.search(":.+",line)
                parsedline['Format'] = res.group(0)[2:-25].replace(",","")    

            if line.startswith('State: '):
                res = re.search(":.+",line)
                parsedline['Bad sectors'] = res.group(0)[30:-12].replace(",","")   
        outfilecsv.writerow(parsedline)

    outfile.close()

if __name__ == "__main__":
    main()
