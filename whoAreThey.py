#!/usr/bin/python
##################################################
## Author: Joshua Franklin
## whoarethey.py
## Example input to start: 
## sudo ./whoarethey.py -f someFileNmae
## The file name should contain an electionBuster results file
## This code relies on a library from Google: https://code.google.com/p/pywhois/
##################################################

import sys
import string
import argparse
import whois

# Function: casts and removes those pesky \r and \n
def stringAndStrip(input): 
	input = str(input)
	input =  input.rstrip()
	return input

#Parse command line arguments
parser = argparse.ArgumentParser(description='Pulls down whois information by parsing a testfile from electionBuster.py')
parser.add_argument('-f','--fileName', help='Name of electionBuster results ,required=True)
args = parser.parse_args()

# Stores command line arguments
# Make all lowercase
fileName = args.fileName

#open inputFile
with open(fileName, 'r') as inputFile:
	lines = list(inputFile)

#open and clear output file
tempResults = 'WHOIS-' + str(fileName) 
resultsFile = open(tempResults, "w")

# This clears the results files before reopening them
resultsFile.close()
resultsFile = open(tempResults, "w")

# Instantiating some variables
totalLines = 0 
index = 0 
positiveResultsLine = 0 
numberOfHits = 0 
URLlist = []

#grabbing total number of lines the file
for line in lines:
	totalLines = totalLines + 1

#finding the line right before the results appear in the file
for line in lines:
	if line[0:13] == 'Total runtime':
		positiveResultsLine = index
	else: 
		index = index + 1

# setting up some more variables
numberOfHits = stringAndStrip(numberOfHits) 
numberOfHits = int(numberOfHits)
positiveResultsLine = positiveResultsLine + 1
hitString = lines[positiveResultsLine]
hitCount = 0 

#increment where we found the results to where URL begin
positiveResultsLine = positiveResultsLine + 5
#parse the hitstring for the number of hits
numberOfHits = hitString[11:13]
index = 0

# parse out the URLs - ridiculously difficult
for line in lines:
	index = index + 1
	if index == positiveResultsLine:
		hitCount = int(numberOfHits)
		URLlist.append(line)
		hitCount = int(hitCount) - 1
		positiveResultsLine = positiveResultsLine + 1
		numberOfHits = int(numberOfHits) - 1
		if hitCount <= 0:
			break

# having some issues with spaces and a dashed line from results file
# basically removing the spaces and dashes, and skipping the first line b/c that's a dash I couldn't get away from
flag = 0 
newList = []
for url in URLlist:
	if flag != 0:
		url = stringAndStrip(url)
		if url != ' ' or '-------------------------------------':
			newList.append(url)
	flag = flag + 1 

#final processing, lookup, and writing to logfile
print 'Printing new URL list'
for url in newList:
	print url
	url = stringAndStrip(url)
	resultsFile.write(str(url) + "\n")
	w = whois.whois(url)
	print w

# Bad things happen if these files are not properly closed
resultsFile.close()

