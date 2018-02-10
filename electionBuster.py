#!/usr/bin/python3.5

 
##################################################
## Author: Joshua Franklin
## Example input to start: 
## sudo ./electionBuster.py -f josh -l franklin -y 2014 -e senate -s pennsyltucky 
## 6 arguments are passed:
## 1: The first name of the candidate
## 2: The last name of the candidate
## 3: The year of the election
## 4: The type of race (e.g., congress, senate, president)
## 5: The state or region the candidate is from
##################################################
# Notes: Move tlds to tryURL such that we try all tlds for each url generated

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
			names = reduce(operator.or_, self.lookup[name])
		return names

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
parser.add_argument('-l','--lastName',help='Candidate\'s last name', required=True)
parser.add_argument('-y','--year', help='Year of the election',required=True)
parser.add_argument('-e','--electionType',help='Type of election (congress, senate, president)', required=True)
parser.add_argument('-s','--state', help='Candidate\'s state of origin')
parser.add_argument('-file','--fileName', help='Filename containing a list of candidates')
args = parser.parse_args()

# Stores command line argumetns
# Make all lowercase
fName = args.firstName
fName = fName.lower()
lName = args.lastName
lName = lName.lower()
year = args.year
electionType = args.electionType
electionType = electionType.lower()
state = ""
if (args.state) :
        state = args.state
        state = stringAndStrip(state)
        state = state.lower()
if (args.fileName) :
        fileName = args.fileName
        fileName = stringAndStrip(fileName)

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
tlds = ['.com', '.net', '.me' , '.org', '.net', '.biz', '.info', '.us', '.ru', '.cn', '.kp' ]

# Runs stringAndStrip on everything except fileName b/c that's used elsewhere
fName = stringAndStrip(fName)
lName = stringAndStrip(lName)
year = stringAndStrip(year)
electionType = stringAndStrip(electionType)
state = stringAndStrip(state)

# Expected URLs (obviously the list is different if the state var exists).
if (args.state) : 
	print('We expect to find these URLs excluding subtle variances:')
	print('http://www.' + fName + lName + '.com')
	print('http://www.' + lName + fName + '.com')
	print('http://www.' + fName + year + '.com')
	print('http://www.' + lName + year + '.com')
	print('http://www.' + fName + lName + year + '.com' )
	print('http://www.' + fName + lName + 'for' + state + '.com')
	print('http://www.' + fName + lName + state + '.com')
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
tempResults = 'results-' + fName + '-' + lName + '-' + state + '-' + str(now) + '.txt'

resultsFile = open(tempResults, "w")

# This clears the results files before reopening them
resultsFile.close()

resultsFile = open(tempResults, "a")

# Need a base alphabet for the first set of mangling functions
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
vowels = "aeiouy"

confirmedURLs = []
testedURLs = []
#skippedURLs = []  Does not appear to be used
allURLS = []
  
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
			'abcdefghijklmnopqrstuvwxyz12e4567890']

# These are the template names - refer to Loop 1 for examples

if (args.state) : 
	templates = [
		fName + lName,
		fName + '-' + lName, 
		lName + fName,
		lName + '-' + fName, 
		fName + year,
		lName + year,
		fName + lName + year, 
		fName + '-' + lName + year, 
		fName + lName + 'for' + state,
		fName + '-' + lName + 'for' + state, 
		fName + lName + '4' + state,
		fName + '-' + lName + '4' + state,
		fName + lName + state, 
		fName + '-' + lName + state, 
		fName + lName + 'for' + position, 
		fName + '-' + lName + 'for' + position, 
		fName + lName + '4' + position,
		fName + '-' + lName + '4' + position,
		fName + 'for' + position,
		fName + '4' + position,
		fName + 'for' + position + year,
		fName + '4' + position + year, 
		position + fName + lName, 
		position + '-' + fName + lName, 
		position + fName + '-' + lName, 
		position + '-' + fName + '-' + lName,
		fName + lName + 'for' + altPosition, 
		fName + lName + '4' + altPosition, 
		fName + 'for' + altPosition,
		fName + '4' + altPosition,
		lName + 'for' + altPosition,
		lName + 'for' + position,
		lName + '4' + position
	]
else :  
	templates = [
		fName + lName,
		fName + '-' + lName, 
		lName + fName,
		lName + '-' + fName, 
		fName + year,
		lName + year,
		fName + lName + year, 
		fName + '-' + lName + year, 
		fName + lName + 'for' + position, 
		fName + '-' + lName + 'for' + position, 
		fName + lName + '4' + position,
		fName + '-' + lName + '4' + position,
		fName + 'for' + position,
		fName + '4' + position,
		fName + 'for' + position + year,
		fName + '4' + position + year, 
		position + fName + lName, 
		position + '-' + fName + lName, 
		position + fName + '-' + lName, 
		'vote' + fName,
		'vote' + lName,
		'votefor' + fName,
		'votefor' + lName,
		'votefor' + fName + lName,
		'vote4' + fName,
		'vote4' + lName,
		'vote4' + fName + lName,
		position + '-' + fName + '-' + lName,
		fName + lName + 'for' + altPosition, 
		fName + lName + '4' + altPosition, 
		fName + 'for' + altPosition,
		fName + '4' + altPosition,
		lName + 'for' + altPosition,
		lName + 'for' + position,
		lName + '4' + position
	]


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
########################
#http://www.donatejoshfranklin.com
#http://wwwjoshfranklin.com

print("Entering template loop 2^^^^^^^^^^^^^^^^^^^^^^^^^^")
#print "There were " + str(len(skippedURLs)) + " skipped so far."
print(time.time() - start_time, "seconds")
for r in results:
	#Donate at the beginning
	tryURL( 'http://www.donate' + r )

	#No period
	tryURL( 'http://www' + r )

### LOOP 3 ###
# Puts donate at the end and removes the period after 'www'
########################
#http://www.joshfranklindonate.com
#http://wwwjoshfranklindonate.com
#print "There were " + str(len(skippedURLs)) + " skipped so far."
print("Entering template loop 3^^^^^^^^^^^^^^^^^^^^^^^^^^" )
print(time.time() - start_time, "seconds")
for r in resultsDonate:
	tryURL( 'http://www.' + r ) # Example: http://www.joshfranklindonate.com
	#Donate at the end without periods after www
	tryURL( 'http://www' + r ) # Example: http://wwwjoshfranklindonate.com

# TODO: add an extra o to situations with two 'o's, like "book" to "boook"
# TODO: try Rick for Richard etcetera 
# TODO: Turn 2014 into 14 so we look for http://www.lName+fName+14.com

### NEW TYPO FUNCTIONS###
# All examples use josh franklin 2014 president DC 

typoFirstLast = fName + lName
typoLastYear= lName + year
typoFirstLastYear = fName + lName + year

vowelResults1 = wrongVowel(typoFirstLast)
skipResults1 = skipLetter(typoFirstLast)
doubleResults1 = doubleLetter(typoFirstLast)
insertResults1 = insertLetter(typoFirstLast)
subResults1 = substitution(typoFirstLast)
reverseResults1 = reverseLetter(typoFirstLast)

vowelResults2 = wrongVowel(typoLastYear)
skipResults2 = skipLetter(typoLastYear)
doubleResults2 = doubleLetter(typoLastYear)
insertResults2 = insertLetter(typoLastYear)
subResults2 = substitution(typoLastYear)
reverseResults2 = reverseLetter(typoLastYear)

vowelResults3 = wrongVowel(typoFirstLastYear)
skipResults3 = skipLetter(typoFirstLastYear)
doubleResults3 = doubleLetter(typoFirstLastYear)
insertResults3 = insertLetter(typoFirstLastYear)
subResults3 = substitution(typoFirstLastYear)
reverseResults3 = reverseLetter(typoFirstLastYear)

### Typo loop 1 ###
#print "There were " + str(len(skippedURLs)) + " skipped so far."
print( "Entering vowel loop")
for r in vowelResults1 : 
	tryURL( 'http://www.' + r )

print("Entering skip loop")
for r in skipResults1 : 
	tryURL( 'http://www.' + r )

print( "Entering double loop")
for r in doubleResults1 : 
	tryURL( 'http://www.' + r )

print("Entering insert loop")
for r in insertResults1 : 
	tryURL( 'http://www.' + r )

print( "Entering sub loop")
for r in subResults1 : 
	tryURL( 'http://www.' + r )

print("Entering reverse loop")
for r in reverseResults1 : 
	tryURL( 'http://www.' + r )
					
### Typo loop 2 ###
#print "There were " + str(len(skippedURLs)) + " skipped so far."
print( "Entering vowel loop")
for r in vowelResults2 : 
	tryURL( 'http://www.' + r )

print( "Entering skip loop")
for r in skipResults2 : 
	tryURL( 'http://www.' + r )

print("Entering double loop")
for r in doubleResults2 : 
	tryURL( 'http://www.' + r )

print("Entering insert loop")
for r in insertResults2 : 
	tryURL( 'http://www.' + r )

print( "Entering sub loop")
for r in subResults2 : 
	tryURL( 'http://www.' + r )

print("Entering reverse loop")
for r in reverseResults2 : 
	tryURL( 'http://www.' + r )

### Typo loop 3 ###
#print "There were " + str(len(skippedURLs)) + " skipped so far."
print( "Entering vowel loop")
for r in vowelResults3 : 
	tryURL( 'http://www.' + r )

print( "Entering skip loop")
for r in skipResults3 : 
	tryURL( 'http://www.' + r )

print( "Entering double loop")
for r in doubleResults3 : 
	tryURL( 'http://www.' + r )

print( "Entering insert loop")
for r in insertResults3 : 
	tryURL( 'http://www.' + r )

print( "Entering sub loop")
for r in subResults3 : 
	tryURL( 'http://www.' + r )

print( "Entering reverse loop")
for r in reverseResults3 : 
	tryURL( 'http://www.' + r )

### CORNER CASES ###
# The following looks for odd domains that I've noticed 
tryURL( 'http://www.team' + fName ) # Example:  'teamfranklin'
tryURL( 'http://www.team' + lName )
tryURL( 'http://www.team' + fName + lName )

# Example:  'repfranklin' 
# It's easier just to include for everyone, even if they are not in a congressional race
tryURL( 'http://www.rep' + fName )
tryURL( 'http://www.rep' + lName )
tryURL( 'http://www.rep' + fName + lName )

#expand the tlds a little
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
tryURL( 'http://www.vote' + fName )           #Example:  votejosh.com
tryURL( 'http://www.vote' + lName )           #Example:  votefranklin.com
tryURL( 'http://www.' + lName + position )    #Example:  franklinpresident.com
tryURL( 'http://www.' + lName + altPosition ) #Example:  franklinprez.com
tryURL( 'http://www.real' + fName + lName )   #Example:  realjoshfranklin.com
tryURL( 'http://www.' + lName + 'for' + state ) #Example:  franklinforDC.com
tryURL( 'http://www.' + lName + '4' + state ) #Example:  franklin4DC.com
tryURL( 'http://www.friendsof' + fName ) #Example:  friendsofjosh.com
tryURL( 'http://www.friendsof' + lName ) #Example:  friendsofjosh.com
tryURL( 'http://www.' + fName + 'sucks' ) #Example:  joshsucks.com
tryURL( 'http://www.' + lName + 'sucks' ) #Example:  franklinsucks.com
tryURL( 'http://www.' + fName )     #Example:  josh.vote
tryURL( 'http://www.' + lName )     #Example:  franklin.vote
tryURL( 'http://www.' + fName + lName ) #Example:  joshfranklin.vote

print( ' Total URLS: ' + str(len(allURLS)) + "\n" )
allURLS = removeDups( allURLS ) 
print( 'Unique URLS: ' + str(len(allURLS)) + "\n" )

pool = ThreadPool(64)
# Open the urls in their own threads
# and return the results
results = pool.map( tryURLforReal, allURLS )
pool.close()
pool.join()
# Each tread added an entry for each result (found or not, gotta filter the blanks)
# I'm doing this here sinced the file writes might not have been synchronized
# its just a fear I had
for i in results:
    if ( len(i) > 10 ) :  
        resultsFile.write( i )

# Wow! You've made it to the end. Well done! 

totalRuntime = time.time() - start_time, "seconds"

###### Write final results to logfile ###########
resultsFile.write( "######################################" + "\n" )
resultsFile.write( "ElectionBuster Scan Results: " + "\n" )
resultsFile.write( "######################################" + "\n" )
resultsFile.write( "INPUTS = " + str(fName) + ", " + str(lName) + ", " + str(year) + ", " + str(electionType) + ", " + str(state) + "\n" )
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
#for url in confirmedURLs:
#	print( url )
#print( "\n" )
#TODO: Parse goodResults.txt's pages and look for GoDaddy, Bluehost pages 

# Bad things happen if these files are not properly closed
resultsFile.close()


