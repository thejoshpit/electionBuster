#!/usr/bin/python3.5

 
##################################################
## Author: Joshua Franklin, Kevin Franklin 
## Example input to start: 
## sudo ./electionBuster.py -f josh -l franklin -y 2014 -e senate -s pennsyltucky 
## 6 arguments are passed:
## 1: The first name of the candidate (mandatory) 
## 2: The middle name of the candidate (optional)
## 2: The last name of the candidate (mandatory)
## 3: The year of the election (mandatory)
## 4: The type of race, such as congress, senate, or president. (mandatory)
## 5: The state or region the candidate is from (optional)
##################################################

#TODO: Add a keyboard interrupt

import requests 
import sys
import time
import string
import argparse
import socket
from datetime import date
import urllib 
from multiprocessing import Pool as ThreadPool, Manager 
import collections
import csv
import operator
from modules.utils import genAllDonate,genAll,generate_urls, tryURLforReal
from modules.text_tools import alphabet,alt_alphabets,skipLetter,stringAndStrip,removeDups,reverseLetter,wrongVowel,tlds

 
confirmedURLs = Manager().list() 

allURLS = Manager().list() 




class NameDenormalizer(object):
	def __init__(self, filename=None):
		filename = filename or 'names.csv'
		lookup = collections.defaultdict(list)
		with open(filename) as f:
			reader = csv.reader(f)
			for line in reader:
				matches = set(line)
				for match in matches:
					lookup[match].append(matches)
		self.lookup = lookup
	def __getitem__(self, name):
		name = name.upper()
		if name not in self.lookup:
			raise KeyError(name)
		return self.lookup[name]

	def get(self, name, default=None):
		try:
			return self[name]
		except KeyError:
			return set( [name] )


# Program Timer
start_time = time.time()

# Function: casts and removes those pesky \r and \n


#Parse command line arguments
parser = argparse.ArgumentParser(description='Identifies registered candidate domains')
parser.add_argument('-f','--firstName', help='Candidate\'s first name',required=True)
parser.add_argument('-m','--middleName',help='Candidate\'s optional middle name')
parser.add_argument('-l','--lastName',help='Candidate\'s last name', required=True)
parser.add_argument('-y','--year', help='Year of the election',required=True)
parser.add_argument('-e','--electionType',help='Type of election (congress, senate, president)', required=True)
parser.add_argument('-s','--state', help='Candidate\'s state of origin', action='append' )
#Exists for candidates like Mitt Romney that possibly have an attachment to two states (i.e., Utah, Massachusetts) 
parser.add_argument('-a','--aliasFileName', help='Filename containing a list of aliases')
parser.add_argument('-p','--party', help='Party Affiliation')
args = parser.parse_args()

# Stores command line argumetns
# Make all lowercase
fName = args.firstName
fName = fName.lower()

lName = args.lastName
lName = lName.lower()
party = ""

year = args.year
shortYear = year[-2:]
electionType = args.electionType
electionType = electionType.lower()
state = []
stateText = ""

if (args.party) :
	party = args.party
fileName = "states.csv"
if (args.aliasFileName) :
        fileName = stringAndStrip( args.aliasFileName)

if (args.state) :
	nd = NameDenormalizer( fileName )
	for aState in args.state:
		stateText = stateText + aState.lower()
		state.append( stringAndStrip( aState.upper( ) ) )
		statenick = list( nd.get( aState.upper() ) )
		for s1 in statenick:
			for s in s1:
				state.append( s )
mName = ""
middleInitial = ""

if (args.middleName) :
	mName = args.middleName
	mName = mName.lower()
	middleInitial = mName[0]

# This assigns the position variable
if (electionType == 'congress') or (electionType == 'congressional') : 
	position = 'congress'
	altPosition = 'congressman'  # congresswoman??
elif electionType == 'senate' : 
	position = 'senator'
	altPosition = 'senate'
elif (electionType == 'governor') or (electionType == 'gubernatorial'): 
	position = 'governor'
	altPosition = 'gov'
elif (electionType == 'president') or (electionType == 'presidential') : 
	position = 'president'
	altPosition = 'prez'
elif (electionType == 'mayoral') or (electionType == 'mayor') : 
	position = 'mayor'
	altPosition = 'mayoral'
else : 
	position = electionType
	altPosition = electionType
	
# top-level domain-names
# # consider removing .me, .info, and .biz if they aren't adding value 


# Runs stringAndStrip on everything except fileName b/c that's used elsewhere
fName = stringAndStrip(fName)
lName = stringAndStrip(lName)
year = stringAndStrip(year)
electionType = stringAndStrip(electionType)

# Alerting the users to the types of sites we're expecting to find 
# This differs at times since the state variable isn't mandatory to run the script 
## Consider deleting this - does it actually provide value? 
if (args.state) : 
	print('We expect to find these URLs excluding subtle variances:')
	print('http://www.' + fName + lName + '.com')
	print('http://www.' + lName + fName + '.com')
	print('http://www.' + fName + year + '.com')
	print('http://www.' + lName + year + '.com')
	print('http://www.' + fName + lName + year + '.com' )
	for stateAlias in state:
		print('http://www.' + fName + lName + 'for' + stateAlias + '.com')
		print('http://www.' + lName + 'for' + stateAlias + '.com')
		print('http://www.' + fName + 'for' + stateAlias + '.com')
	print('http://www.' + fName + lName + 'for' + position + '.com')
	print('http://www.' + fName + 'for' + position + '.com')
	print('http://www.' + fName + 'for' + position + year + '.com')
	print('http://www.' + position + fName + lName + '.com')
else : 
	print('We expect to find these URLs excluding subtle variances:')
	print('http://www.' + fName + lName + '.com')
	print('http://www.' + lName + fName + '.com')
	print('http://www.' + fName + year + '.com')
	print('http://www.' + lName + year + '.com')
	print('http://www.' + fName + lName + year + '.com' )
	print('http://www.' + fName + lName + 'for' + position + '.com')
	print('http://www.' + fName + 'for' + position + '.com')
	print('http://www.' + fName + 'for' + position + year + '.com')
	print('http://www.' + position + fName + lName + '.com')

# This is the result output files
# Makes a unique filename based on data and time
now = date.today()
partyString = ""
if ( args.party ) :
	partyString = "-" + party.lower()
	
tempResults = 'results-' + fName + '-' + lName + '-' + stateText + partyString + '-' + str(now) + '.txt'

resultsFile = open(tempResults, "w")

# This clears the results files before reopening them
resultsFile.close()

resultsFile = open(tempResults, "a")


## Other alphabets are defined as a quick way of doing URL mangling. 
## Is this a candidate for deletion? 
# alternative alphabets 
# 0: No change
# 1: i -> 1 "Eye to One"
# 2: l -> i "El to Eye"
# 3: i -> l "Eye to El"
# 4: o -> 0 "Oh to Zero"
# 5: 0 -> o "Zero to Oh" 
# 6: n -> m "En to Em" TODO: Does this swap wrok right? 
# 7: m -> n "Em to En"
# 8: e -> 3 "Ee to three"
# 9: 3 -> e "Three to ee"


# These are the template that we'll use based on the optional input parameters. 
# The first one is if the state was input. 
templates = generate_urls(first_name=args.firstName,
						  last_name=args.lastName,
						  state=state,
						  middlename=args.middleName,
						  position=position,
						  altPosition=altPosition,
						  year=args.year)


# This generates the text mangling
results = genAll(templates, alt_alphabets)

# This generates the text mangling with some other alternatives
resultsDonate = genAllDonate(templates, alt_alphabets)

#### LOOP 1 ####
# All examples use the input of 'josh franklin 2014 president DC' 
#################
#http://www.joshfranklin.com
#http://www.josh2014.com
#http://www.franklin2014.com
#http://www.joshfranklin2014.com
#http://www.joshfranklinforDC.com
#http://www.joshfranklinDC.com
#http://www.joshforpresident.com
#http://www.josh4president.com
#http://www.joshforpresident2014.com
#http://www.josh4president2014.com
#http://www.presidentjoshfranklin.com
#http://www.president-josh-franklin.com
#http://www.presidentjoshforpresident2014.com
#http://www.presidentjosh4president2014.com
#http://www.presidentjoshfranklinforpresident2014.com
#http://www.presidentjosh-franklinforpresident2014.com
#http://www.presidentjoshfranklin4president2014.com
#http://www.presidentjosh-franklin4president2014.com

def tryURL(url):
	url = stringAndStrip(url)
	for domain_name in tlds:
		print('Trying: ' + url + domain_name)
		allURLS.append(url + domain_name)


print("Entering template loop 1^^^^^^^^^^^^^^^^^^^^^^^^^^" )
print(time.time() - start_time, "seconds")
for r in results:
	tryURL( 'http://www.' + r , )

### LOOP 2 ###
# Puts donate at the beginning & 
# Removes the period after 'www'
##############tlds a little
tlds.append( '.republican' )
tlds.append( '.democrat' )
tlds.append( '.red' )
tlds.append( '.blue' )
tlds.append( '.vote' )

#These next few look for some of the larger parties
tryURL( 'http://www.republican' + fName + lName )
tryURL( 'http://www.democrat' + fName + lName )
tryURL( 'http://www.libertarian' + fName + lName )
tryURL( 'http://www.independent' + fName + lName )
tryURL( 'http://www.vote' + fName + lName )   #Example:  votejoshfranklin.com
tryURL( 'http://www.vote' + fName + middleInitial + lName )   #Example:  votejoshmichaelfranklin.com
tryURL( 'http://www.vote' + fName )           #Example:  votejosh.com
tryURL( 'http://www.vote' + lName )           #Example:  votefranklin.com
tryURL( 'http://www.' + lName + position )    #Example:  franklinpresident.com
tryURL( 'http://www.' + lName + altPosition ) #Example:  franklinprez.com
tryURL( 'http://www.real' + fName + lName )   #Example:  realjoshfranklin.com
for stateAlias in state:
	tryURL( 'http://www.' + lName + 'for' + stateAlias ) #Example:  franklinforDC.com
	tryURL( 'http://www.' + lName + '4' + stateAlias ) #Example:  franklin4DC.com
tryURL( 'http://www.friendsof' + fName ) #Example:  friendsofjosh.com
tryURL( 'http://www.friendsof' + lName ) #Example:  friendsofjosh.com
tryURL( 'http://www.' + fName + 'sucks' ) #Example:  joshsucks.com
tryURL( 'http://www.' + lName + 'sucks' ) #Example:  franklinsucks.com
tryURL( 'http://www.' + fName )     #Example:  josh.vote
tryURL( 'http://www.' + lName )     #Example:  franklin.vote
tryURL( 'http://www.' + fName + lName ) #Example:  joshfranklin.vote
tryURL( 'http://www.elect' + fName + lName )
tryURL( 'http://www.elect' + fName + middleInitial + lName )
tryURL( 'http://www.elect' + fName )
tryURL( 'http://www.elect' + lName )
tryURL( 'http://www.' + fName + middleInitial + year )
tryURL( 'http://www.' + middleInitial + lName )


print( ' Total URLS: ' + str(len(allURLS)) + "\n" )
allURLS = removeDups( allURLS ) 
print( 'Unique URLS: ' + str(len(allURLS)) + "\n" )

pool = ThreadPool( 24 )

# Open the urls in their own threads
# and return the results
results = pool.map( tryURLforReal, allURLS )
pool.close()
pool.join()

#print(results)
# Each thread added an entry for each result (found or not, gotta filter the blanks)
# I'm doing this here sinced the file writes might not have been synchronized
# its just a fear I had
for i in results:
    resultsFile.write( i )

totalRuntime = time.time() - start_time, "seconds"

###### Write final results to logfile ###########
resultsFile.write( "######################################" + "\n" )
resultsFile.write( "ElectionBuster Scan Results: " + "\n" )
resultsFile.write( "######################################" + "\n" )
resultsFile.write( "INPUTS = " + str(fName) + ", " + str(mName) + ", " + str(lName) + ", " + str(year) + ", " + str(position) + ", " + str(altPosition) + ", " + str(stateText) + ", " + str(party) + "\n" )

resultsFile.write( "Total runtime was " + str(totalRuntime) + "\n" )
resultsFile.write( "There were " + str(len(confirmedURLs)) + " positive results." + "\n" )
resultsFile.write( "There were " + str(len(testedURLs)) + " unique URLs tested." + "\n" )
resultsFile.write( "-------------------------------------" + "\n" )
resultsFile.write( "Positive results: " + "\n" )
resultsFile.write( "-------------------------------------" + "\n" )
for url in confirmedURLs:
	resultsFile.write( str(url) + "\n" )
resultsFile.write( "\n" )
resultsFile.write( "-------------------------------------" + "\n" )
resultsFile.write( "EOF " + "\n" )
#for url in allURLS:
#	resultsFile.write( str(url) + "\n" )
#	print( str( url ) + "\n" )
	
###### Print final results to screen ###########	 		
print( "###################################### " + "\n" )
print( "ElectionBuster Scan Results: " + "\n" )
print( "###################################### " + "\n" )
print( "INPUTS" + "\n" )
print( "First name: " + fName + "\n" )
print( "Middle name: " + mName + "\n" )
print( "Last name: " + lName + "\n" )
print( "Year: " + year + "\n" )
print( "Election type: " + electionType + "\n" )
print( "-------------------------------------" + "\n" )
print( "Total runtime was " + str(totalRuntime) + "\n" )
print( "-------------------------------------" + "\n" )
 
print( "Positive results: " + "\n" )
print( "There were " + str(len(confirmedURLs)) + " hits:" + "\n" )
print( "-------------------------------------" + "\n" )
print( "\n" )
for url in confirmedURLs:
	print( url )
print( "\n" )


# Bad things happen if these files are not properly closed
resultsFile.close()

