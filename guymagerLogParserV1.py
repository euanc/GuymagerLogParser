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
    fieldnames = ['Case number','Evidence number', 'Examiner', 'File Path','Format',
                  'Number of Bytes','Date of acquisition', 'Time taken', 'MD5 Hash Verified Image',
                  'Bad sectors']
    outfilecsv = csv.DictWriter(outfile, fieldnames=fieldnames)
    outfilecsv.writeheader()

    files = glob(os.path.join(args.inputdir, '*.info'))

    for filename in files:
        parsedline = {}
        for line in open(filename, 'rU'): 

            if line.strip().startswith('Case number'):
                parsedline['Case number'] = line[26:].strip()

            if line.strip().startswith('Evidence number'):
                parsedline['Evidence number'] = line[26:].strip()

            if line.strip().startswith('Examiner'):
                parsedline['Examiner'] = line[26:].strip()
                
            if line.strip().startswith('Image path and file name'):
                parsedline['File Path'] = line[26:].strip()
            
            if line.strip().startswith('Device size'):
                parsedline['Number of Bytes'] = line[26:].split()[0]
                
            if line.strip().startswith('Ended'):
                parsedline['Date of acquisition'] = line[22:41]
                elapsed = re.match('(\d+) hours, (\d+) minutes and (\d+) seconds', line[43:].strip())
                elapsedtotal = (3600*int(elapsed.group(1))) + (60*int(elapsed.group(2))) + int(elapsed.group(3))
                parsedline['Time taken'] = elapsedtotal
                
            if line.strip().startswith('MD5 hash verified image'):
                parsedline['MD5 Hash Verified Image'] = line[28:].strip()
            # NOTE: If the disk image format chosen is not raw (dd) this value will not match
            #       the hash value of the disk image file created.
                
            if line.strip().startswith('Format'):
                parsedline['Format'] = line[26:].strip()

            if line.strip().startswith('State'):
                badsectors = re.search('with (\d+) bad sectors', line)
                if badsectors:
                    badsectorcount = badsectors.group(1)
                else:
                    badsectorcount = '0'
                parsedline['Bad sectors'] = badsectorcount

        outfilecsv.writerow(parsedline)

    outfile.close()

if __name__ == "__main__":
    main()
