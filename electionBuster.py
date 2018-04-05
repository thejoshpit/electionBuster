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

import requests 
import sys
import time
import string
import argparse
import socket
from datetime import date
import urllib 
from multiprocessing import Pool as ThreadPool 
import collections
import csv
import operator

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
def stringAndStrip(input): 
	input = str(input)
	input =  input.rstrip()
	return input

def tryURL(url) :
	url = stringAndStrip(url)
	for domain_name in tlds:
		print('Trying: ' + url + domain_name )
		allURLS.append( url + domain_name )
	
def tryURLforReal(url) : 
	fetchResult = ""
	if url not in testedURLs :
		testedURLs.append(url)
		try: 
			#Open input URL
			httpResponse = requests.get(url, timeout=10)
			fetchResult =               "*************************************************+" + "\n" 
			fetchResult = fetchResult + "Page Exists: " + httpResponse.url + "\n"
			fetchResult = fetchResult + str(url) + ", " + str(httpResponse.status_code) + "\n"
			fetchResult = fetchResult + str(httpResponse.headers) + "\n"
			fetchResult = fetchResult + "*************************************************+" + "\n"
			print(fetchResult)
			confirmedURLs.append(url)

			return fetchResult 
		except requests.exceptions.RequestException as e:    # This is the correct syntax
                    pass
		except socket.timeout as e:
                    pass
	return fetchResult

def removeDups(numbers):
    newlist = []
    for number in numbers:
       if number not in newlist:
           newlist.append(number)
    return newlist

def gen(website_name, alt_alphabet):
        A = 'abcdefghijklmnopqrstuvwxyz1234567890' # original alphabet string
        xform = str.maketrans(A, alt_alphabet)
        s = website_name.translate(xform)
        return s

def genAll(website_names, alphabets):
	results = []
	for s in website_names:
		for a in alphabets:
			mangled_name = gen(s, a)
			results.append( mangled_name )
	return results

def genAllDonate(website_names, alphabets):
	results = []
	for s in website_names:
		for a in alphabets:
			mangled_name = gen(s, a)
			results.append( mangled_name + 'donate' )
	return results

# This function returns strings with each character missing
#['oshua', 'jshua', 'johua', 'josua', 'josha', 'joshu']
def skipLetter(s):
        kwds = []

        for i in range(1, len(s)+1):
            kwds.append(s[:i-1] + s[i:])
        return kwds

# This function subsitutes the wrong vowell for each letter
#'aoshua', 'boshua', 'coshua', 'doshua'
def wrongVowel(s):
        kwds = []
        for i in range(0, len(s)):
            for letter in vowels:
                if s[i] in vowels:
                    for vowel in vowels:
                        s_list = list(s)
                        s_list[i] = vowel
                        kwd = "".join(s_list)
                        kwds.append(kwd)
        return kwds

# This function inserts each alphabetic character into each place in a word
#['ajoshua', 'jjoshua', 'jooshua', 'josshua', 'joshhua', 'joshuua', 'joshuaa']
def doubleLetter(s):
        kwds = []
        for i in range(0, len(s)+1):
            kwds.append(s[:i] + s[i-1] + s[i:])

        return kwds

# This function inserts each alphabetic character into each place in a word
#'jaoshua', 'jnoshua', 'josthua', 'joshuza', 'joshua2'
def insertLetter(s):
       
        kwds = []

        for i in range(0, len(s)):
            for char in alphabet:
                kwds.append(s[:i+1] + char + s[i+1:])

        return kwds

# This function reverses each letter
#['ojshua', 'jsohua', 'johsua', 'josuha', 'joshau']
def reverseLetter(s):
        kwds = []
        for i in range(0, len(s)):
            letters = s[i-1:i+1:1]
            if len(letters) != 2:
                continue

            reverse_letters = letters[1] + letters[0]
            kwds.append(s[:i-1] + reverse_letters + s[i+1:])

        return kwds
        
#'aoshua', josh9a', 'josqua', 'jzshua'        
def substitution(s):
        kwds = []

        for i in range(0, len(s)):
            for letter in alphabet:
                kwd = s[:i] + letter + s[i+1:]
                kwds.append(kwd)
                
        return kwds      

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
tlds = ['.com', '.net', '.me' , '.org', '.net', '.biz', '.info', '.us', '.cm' ]

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

# Need a base alphabet for the first set of mangling functions
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"

#sometimes "y" because it makes kevin angry 
vowels = "aeiouy"

confirmedURLs = []
testedURLs = []
allURLS = []

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

alt_alphabets = [ 	'abcdefghijklmnopqrstuvwxyz1234567890',
			'abcdefgh1jklmnopqrstuvwxyz1234567890',
			'abcdefghijkimnopqrstuvwxyz1234567890',
			'abcdefghljklmnopqrstuvwxyz1234567890',
			'abcdefghijklmn0pqrstuvwxyz1234567890',
			'abcdefghijklmnopqrstuvwxyz123456789o',
			'abcdefghijklmmopqrstuvwxyz1234567890',
			'abcdefghijklnnopqrstuvwxyz1234567890',
			'abcd3fghijklmnopqrstuvwxyz1234567890',
			'Аbcdefghijklmnopqrstuvwxyz1234567890', # homographic Cyrillic А
			'аbcdefghijklmnopqrstuvwxyz1234567890', # homographic Cyrillic а
			'Ӓbcdefghijklmnopqrstuvwxyz1234567890', # homographic Cyrillic Ӓ 
			'ӓbcdefghijklmnopqrstuvwxyz1234567890', # homographic Cyrillic ӓ 
			'Αbcdefghijklmnopqrstuvwxyz1234567890', # homographic Greek Α
			'abcdefghijklmnОpqrstuvwxyz1234567890', # homographic Cyrillic О
			'abcdefghijklmnоpqrstuvwxyz1234567890', # homographic Cyrillic о   
			'abcdefghijklmnоpqrstuvwxyz1234567890', # homographic Greek о  
			'abcdefghijklmnopqrsΤuvwxyz1234567890',	# homographic Greek Τ  
			'abcdefghijklmnopqrsТuvwxyz1234567890',	# homographic Cyrillic Т	
			'abcdefghijklΜnopqrstuvwxyz1234567890',	# homographic Greek Μ	
			'abcdefghijklМnopqrstuvwxyz1234567890',	# homographic Cyrillic М	
			'abcdefghijklmnoРqrstuvwxyz1234567890',	# homographic Cyrillic Р
			'abcdefghijklmnoРqrstuvwxyz1234567890',	# homographic Cyrillic Р		
			'abcdefghijklmnopqrstuvwxyz12e4567890']

# These are the template that we'll use based on the optional input parameters. 
# The first one is if the state was input. 
if (args.state) : 
	templates = []
	templates.append( fName + lName )
	templates.append( fName + '-' + lName )
	templates.append( lName + fName )
	templates.append( lName + '-' + fName )
	templates.append( fName + year )
	templates.append( fName + shortYear )
	templates.append( lName + year )
	templates.append( lName + shortYear )	
	templates.append( fName + lName + year )
	templates.append( fName + lName + shortYear )	
	templates.append( fName + '-' + lName + year )
	templates.append( fName + '-' + lName + shortYear )	
	for stateAlias in state:
		templates.append( fName + lName + 'for' + stateAlias )
		templates.append( fName + lName + 'for' + stateAlias + year)
		templates.append( fName + lName + 'for' + stateAlias + shortYear)	
		templates.append( lName + 'for' + stateAlias )
		templates.append( lName + 'for' + stateAlias + year)
		templates.append( lName + 'for' + stateAlias + shortYear)
		templates.append( fName + 'for' + stateAlias )
		templates.append( fName + 'for' + stateAlias + year)
		templates.append( fName + 'for' + stateAlias + shortYear)
		templates.append( fName + '-' + lName + 'for' + stateAlias )
		templates.append( fName + lName + '4' + stateAlias )
		templates.append( fName + '-' + lName + '4' + stateAlias )
		templates.append( fName + lName + stateAlias )
		templates.append( fName + '-' + lName + stateAlias )
	templates.append( fName + lName + 'for' + position )
	templates.append( fName + '-' + lName + 'for' + position )
	templates.append( fName + lName + '4' + position )
	templates.append( fName + '-' + lName + '4' + position )
	templates.append( fName + 'for' + position )
	templates.append( fName + '4' + position )
	templates.append( fName + 'for' + position + year )
	templates.append( fName + 'for' + position + shortYear )
	templates.append( fName + '4' + position + year )
	templates.append( fName + '4' + position + shortYear )	
	templates.append( position + fName + lName )
	templates.append( position + '-' + fName + lName )
	templates.append( position + fName + '-' + lName )
	templates.append( position + '-' + fName + '-' + lName )
	templates.append( fName + lName + 'for' + altPosition )
	templates.append( fName + lName + '4' + altPosition )
	templates.append( fName + 'for' + altPosition )
	templates.append( fName + '4' + altPosition )
	templates.append( lName + 'for' + altPosition )
	templates.append( lName + 'for' + position )
	templates.append( lName + '4' + position )
# This one is for middle name only 
elif (args.middleName):  
	templates = []
	templates.append( fName + lName )
	templates.append( fName + mName + lName )
	templates.append( fName + middleInitial + lName )
	templates.append( fName + '-' + lName )
	templates.append( lName + fName )
	templates.append( lName + '-' + fName )
	templates.append( fName + year )
	templates.append( lName + year )
	templates.append( fName + lName + year )
	templates.append( fName + '-' + lName + year )
	templates.append( fName + lName + 'for' + position )
	templates.append( fName + '-' + lName + 'for' + position )
	templates.append( fName + lName + '4' + position )
	templates.append( fName + '-' + lName + '4' + position )
	templates.append( fName + mName + 'for' + position )
	templates.append( fName + mName + year)
	templates.append( fName + middleInitial + year )
	templates.append( fName + mName + 'for' + position + year)
	templates.append( fName + middleInitial + 'for' + position + year )
	templates.append( fName + middleInitial + 'for' + position )
	templates.append( fName + 'for' + position )
	templates.append( fName + '4' + position )
	templates.append( fName + 'for' + position + year )
	templates.append( fName + '4' + position + year )
	templates.append( position + fName + lName )
	templates.append( position + '-' + fName + lName )
	templates.append( position + fName + '-' + lName )
	templates.append( position + '-' + fName + '-' + lName )
	templates.append( fName + lName + 'for' + altPosition )
	templates.append( fName + lName + '4' + altPosition )
	templates.append( fName + 'for' + altPosition )
	templates.append( fName + '4' + altPosition )
	templates.append( lName + 'for' + altPosition )
	templates.append( lName + 'for' + position )
	templates.append( lName + '4' + position )
#This one is middle name and state 
elif (args.middleName and args.state):  
	templates = []
	templates.append( fName + lName )
	templates.append( fName + mName + lName )
	templates.append( fName + middleInitial + lName )
	templates.append( fName + '-' + lName )
	templates.append( lName + fName )
	templates.append( lName + '-' + fName )
	templates.append( fName + year )
	templates.append( fName + shortYear )
	templates.append( lName + year )
	templates.append( lName + shortYear )
	templates.append( fName + lName + year )
	templates.append( fName + lName + shortYear )	
	templates.append( fName + '-' + lName + year )
	templates.append( fName + '-' + lName + shortYear )	
	for stateAlias in state:
		templates.append( fName + lName + 'for' + stateAlias )
		templates.append( fName + lName + 'for' + stateAlias + year)
		templates.append( fName + lName + 'for' + stateAlias + shortYear)	
		templates.append( lName + 'for' + stateAlias )
		templates.append( lName + 'for' + stateAlias + year)
		templates.append( lName + 'for' + stateAlias + shortYear)
		templates.append( fName + '-' + lName + 'for' + stateAlias )
		templates.append( fName + lName + '4' + stateAlias )
		templates.append( fName + '-' + lName + '4' + stateAlias )
		templates.append( fName + lName + stateAlias )
		templates.append( fName + '-' + lName + stateAlias )
	templates.append( fName + lName + 'for' + position )
	templates.append( fName + '-' + lName + 'for' + position )
	templates.append( fName + lName + '4' + position )
	templates.append( fName + '-' + lName + '4' + position )
	templates.append( fName + mName + 'for' + position )
	templates.append( fName + mName + year)
	templates.append( fName + mName + shortYear)	
	templates.append( fName + middleInitial + year )
	templates.append( fName + middleInitial + shortYear )	
	templates.append( fName + mName + 'for' + position + year)
	templates.append( fName + mName + 'for' + position + shortYear)	
	templates.append( fName + middleInitial + 'for' + position + year )
	templates.append( fName + middleInitial + 'for' + position + shortYear )	
	templates.append( fName + middleInitial + 'for' + position )
	templates.append( fName + 'for' + position )
	templates.append( fName + '4' + position )
	templates.append( fName + 'for' + position + year )
	templates.append( fName + 'for' + position + shortYear )	
	templates.append( fName + '4' + position + year )
	templates.append( fName + '4' + position + shortYear )	
	templates.append( position + fName + lName )
	templates.append( position + '-' + fName + lName )
	templates.append( position + fName + '-' + lName )
	templates.append( position + '-' + fName + '-' + lName )
	templates.append( fName + lName + 'for' + altPosition )
	templates.append( fName + lName + '4' + altPosition )
	templates.append( fName + 'for' + altPosition )
	templates.append( fName + '4' + altPosition )
	templates.append( lName + 'for' + altPosition )
	templates.append( lName + 'for' + position )
	templates.append( lName + '4' + position )
#this one is the least number of parameters, just the basics 
else :  
	templates = []
	templates.append( fName + lName )
	templates.append( fName + '-' + lName )
	templates.append( lName + fName )
	templates.append( lName + '-' + fName )
	templates.append( fName + year )
	templates.append( fName + shortYear )
	templates.append( lName + year )
	templates.append( lName + shortYear )
	templates.append( fName + lName + year )
	templates.append( fName + lName + shortYear )
	templates.append( fName + '-' + lName + year )
	templates.append( fName + '-' + lName + shortYear )	
	templates.append( fName + lName + 'for' + position )
	templates.append( fName + '-' + lName + 'for' + position )
	templates.append( fName + lName + '4' + position )
	templates.append( fName + '-' + lName + '4' + position )
	templates.append( fName + 'for' + position )
	templates.append( fName + '4' + position )
	templates.append( fName + 'for' + position + year )
	templates.append( fName + 'for' + position + shortYear )
	templates.append( fName + '4' + position + year )
	templates.append( fName + '4' + position + shortYear )	
	templates.append( fName + 'for' + position + year )
	templates.append( lName + 'for' + position + shortYear )
	templates.append( lName + '4' + position + year )
	templates.append( lName + '4' + position + shortYear )
	templates.append( position + fName + lName )
	templates.append( position + '-' + fName + lName )
	templates.append( position + fName + '-' + lName )
	templates.append( 'vote' + fName )
	templates.append( 'vote' + lName )
	templates.append( 'votefor' + fName )
	templates.append( 'votefor' + lName )
	templates.append( 'votefor' + fName + lName )
	templates.append( 'vote4' + fName )
	templates.append( 'vote4' + lName )
	templates.append( 'vote4' + fName + lName )
	templates.append( position + '-' + fName + '-' + lName )
	templates.append( fName + lName + 'for' + altPosition )
	templates.append( fName + lName + '4' + altPosition )
	templates.append( fName + 'for' + altPosition )
	templates.append( fName + '4' + altPosition )
	templates.append( lName + 'for' + altPosition )
	templates.append( lName + 'for' + position )
	templates.append( lName + '4' + position )


# This generates the text mangling
results = genAll( templates, alt_alphabets)

# This generates the text mangling with some other alternatives
resultsDonate = genAllDonate( templates, alt_alphabets)

#### LOOP 1 ####
# All examples use the input of 'josh franklin 2014 president DC' 
##################
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

print("Entering template loop 1^^^^^^^^^^^^^^^^^^^^^^^^^^" )
print(time.time() - start_time, "seconds")
for r in results:
	tryURL( 'http://www.' + r )

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

pool = ThreadPool(64)

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
resultsFile.write( "INPUTS = " + str(fName) + ", " + str(lName) + ", " + str(year) + ", " + str(electionType) + ", " + str(stateText) + "\n" )
resultsFile.write( "Total runtime was " + str(totalRuntime) + "\n" )
#resultsFile.write( "There were " + str(len(confirmedURLs)) + " positive results." + "\n" )
#resultsFile.write( "There were " + str(len(testedURLs)) + " unique URLs tested." + "\n" )
#resultsFile.write( "-------------------------------------" + "\n" )
#resultsFile.write( "Positive results: " + "\n" )
#resultsFile.write( "-------------------------------------" + "\n" )
#for url in confirmedURLs:
#	resultsFile.write( str(url) + "\n" )
resultsFile.write( "\n" )
resultsFile.write( "-------------------------------------" + "\n" )
resultsFile.write( "EOF " + "\n" )
for url in allURLS:
	resultsFile.write( str(url) + "\n" )
	
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
## TODO: Currently not displayed due to bug 
print( "Positive results: " + "\n" )
print( "There were " + str(len(confirmedURLs)) + " hits:" + "\n" )
print( "-------------------------------------" + "\n" )
print( "\n" )
#for url in confirmedURLs:
#	print( url )
#print( "\n" )


# Bad things happen if these files are not properly closed
resultsFile.close()


