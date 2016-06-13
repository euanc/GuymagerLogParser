GuymagerLogParser
=================

Script to parse/process guymager logs in bulk


This python (tested on 2.7) program/script will take a set of input Guymager log files and process them to extract the following into a CSV file:

* Case number
* Evidence number
* Examiner
* File Path
* Format
* Number of Bytes
* Date of acquisition
* Time taken
* MD5 Hash
* Bad sectors

It is useful mostly for doing summary stats, e.g. how many disks had bad sectors? How many bad sectors in total across all disks? How long did it take to image the disks?

It does this by looking at the beginning of each line in the file and matching those with the information we want to extract based on how the lines begin. Eg. it searches for the line that starts with "   Case number". Then slices out just the relevant information from that line. 

You can use this to bulk process a folder full of guymager logs by invoking the script/program with two parameters:

Firstly, the source directory (where the logs are) and secondly the destination file where you would like the CSV file with the results to go.  (This will not overwrite existing files, so choose something that doesn't already exist.)

e.g. in Windows you might use this at the command line (without quotes):

"c:\python27\python.exe d:\logs\guymagerLogParserV1.py d:\logs\diskImages\ d:\logs\guymager_stats.csv"

Where you have:
* python 2.7 installed in the default location
* the program in d:\logs\ 
* the logs to process in d:\logs\diskImages\
* the output CSV desired location is d:\logs\guymager_stats.csv
