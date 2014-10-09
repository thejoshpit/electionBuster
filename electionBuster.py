#!/usr/bin/python
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

import sys
import time
import string
import argparse
from datetime import date
from urllib2 import Request, urlopen, URLError, HTTPError

# Program Timer
start_time = time.time()

# Function: casts and removes those pesky \r and \n
def stringAndStrip(input): 
	input = str(input)
	input =  input.rstrip()
	return input

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
	altPosition = 'congressman'
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

# Runs stringAndStrip on everything except fileName b/c that's used elsewhere
fName = stringAndStrip(fName)
lName = stringAndStrip(lName)
year = stringAndStrip(year)
electionType = stringAndStrip(electionType)
state = stringAndStrip(state)

# Expected URLs (obviously the list is different is the state var exists).
if (args.state) : 
	print 'We expect to find these URLs excluding subtle variances:'
	print 'http://www.' + fName + lName + '.com'
	print 'http://www.' + lName + fName + '.com'
	print 'http://www.' + fName + year + '.com'
	print 'http://www.' + lName + year + '.com'
	print 'http://www.' + fName + lName + year + '.com' 
	print 'http://www.' + fName + lName + 'for' + state + '.com'
	print 'http://www.' + fName + lName + state + '.com'
	print 'http://www.' + fName + lName + 'for' + position + '.com'
	print 'http://www.' + fName + 'for' + position + '.com'
	print 'http://www.' + fName + 'for' + position + year + '.com'
	print 'http://www.' + position + fName + lName + '.com'
else : 
	print 'We expect to find these URLs excluding subtle variances:'
	print 'http://www.' + fName + lName + '.com'
	print 'http://www.' + lName + fName + '.com'
	print 'http://www.' + fName + year + '.com'
	print 'http://www.' + lName + year + '.com'
	print 'http://www.' + fName + lName + year + '.com' 
	print 'http://www.' + fName + lName + 'for' + position + '.com'
	print 'http://www.' + fName + 'for' + position + '.com'
	print 'http://www.' + fName + 'for' + position + year + '.com'
	print 'http://www.' + position + fName + lName + '.com'

# This is the result output files
# Makes a unique filename based on data and time
now = date.today()
tempResults = 'results-' + fName + '-' + lName + str(now) + '.txt'

resultsFile = open(tempResults, "w")

# This clears the results files before reopening them
resultsFile.close()

resultsFile = open(tempResults, "a")

# Need a base alphabet for the first set of mangling functions
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
vowels = "aeiouy"

confirmedURLs = []
testedURLs = []
skippedURLs = []

def tryURL(url) : 
	url = url
	if url not in testedURLs :
		try: 
			#Open input URL
			httpResponse = urlopen(url)
			print "*********************************************************************"
			print "Page Exists: " + httpResponse.geturl() + "."
			print httpResponse.info()
			print httpResponse.code
			print "*********************************************************************"
			confirmedURLs.append(url)
			testedURLs.append(url)
			resultsFile.write("*************************************************+" + "\n")
			resultsFile.write("Page Exists: " + httpResponse.geturl() + "\n")
			resultsFile.write(str(url) + ", " + str(httpResponse.code) + "\n")
			resultsFile.write(str(httpResponse.info()) + "\n")
			resultsFile.write("*************************************************+" + "\n")
						
		except HTTPError, e: 
			print "HTTPError"
			print e
			print e.code
			resultsFile.write(str(url) + ", HTTPError, " + str(e.code) + "\n")
			testedURLs.append(url)
			skippedURLs.append(url)
		except URLError, e: 
			print "URLError"
			print e.reason
			resultsFile.write(str(url) + ", URLError, " + str(e.reason) + "\n")
			testedURLs.append(url)
			skippedURLs.append(url)

def gen(website_name, alt_alphabet):
        A = 'abcdefghijklmnopqrstuvwxyz1234567890' # original alphabet string
        xform = string.maketrans(A, alt_alphabet)
        s = website_name.translate(xform)
        return s

def genAll(website_names, alphabets):
        results = []
        for s in website_names:
                for a in alphabets:
                        mangled_name = gen(s, a)
                        for domain_name_ending in tlds:
                                results.append( mangled_name + '.' + domain_name_ending )
	return results

def genAllDonate(website_names, alphabets):
        results = []
        for s in website_names:
                for a in alphabets:
                        mangled_name = gen(s, a)
                        for domain_name_ending in tlds:
                                results.append( mangled_name + 'donate.' + domain_name_ending )
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

alt_alphabets = [ 'abcdefghijklmnopqrstuvwxyz1234567890',
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
				 position + '-' + fName + '-' + lName,
				 fName + lName + 'for' + altPosition, 
				 fName + lName + '4' + altPosition, 
				 fName + 'for' + altPosition,
				 fName + '4' + altPosition,
				 lName + 'for' + altPosition,
				 lName + 'for' + position,
				 lName + '4' + position
				 ]

# top-level domain-names
tlds = ['com', 'net', 'me' , 'org', 'net', 'biz', 'info', 'us' ]

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

print "Entering template loop 1^^^^^^^^^^^^^^^^^^^^^^^^^^" 
print time.time() - start_time, "seconds"
for r in results:
	r = stringAndStrip(r) 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	print 'Trying: ' + url
	tryURL(url)

### LOOP 2 ###
# Puts donate at the beginning & 
# Removes the period after 'www'
########################
#http://www.donatejoshfranklin.com
#http://wwwjoshfranklin.com

print "Entering template loop 2^^^^^^^^^^^^^^^^^^^^^^^^^^"
print "There were " + str(len(skippedURLs)) + " skipped so far."
print time.time() - start_time, "seconds"
for r in results:
	r = stringAndStrip(r) 
	
	#Donate at the beginning
	url = 'http://www.donate' + r
	url = stringAndStrip(url)
	print 'Trying: ' + url
	tryURL(url)

	#No period
	urlnoperiod = 'http://www' + r
	url = stringAndStrip(urlnoperiod)
	print 'Trying: ' + urlnoperiod
	tryURL(urlnoperiod)

### LOOP 3 ###
# Puts donate at the end and removes the period after 'www'
########################
#http://www.joshfranklindonate.com
#http://wwwjoshfranklindonate.com
print "There were " + str(len(skippedURLs)) + " skipped so far."
print "Entering template loop 3^^^^^^^^^^^^^^^^^^^^^^^^^^" 
print time.time() - start_time, "seconds"
for r in resultsDonate:
	r = stringAndStrip(r) 
	
	#http://www.joshfranklindonate.com
	url = 'http://www.' + r
	url = stringAndStrip(url)
	print 'Trying: ' + url
	tryURL(url)
	
	#Donate at the end without periods after www
	#http://wwwjoshfranklindonate.com
	urlnoperiod = 'http://www' + r 
	url = stringAndStrip(urlnoperiod)
	print 'Trying: ' + urlnoperiod
	tryURL(urlnoperiod)

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
print "There were " + str(len(skippedURLs)) + " skipped so far."
print "Entering vowel loop"
for r in vowelResults1 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)

print "Entering skip loop"
for r in skipResults1 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)	

print "Entering double loop"
for r in doubleResults1 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)	

print "Entering insert loop"
for r in insertResults1 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)		

print "Entering sub loop"
for r in subResults1 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)	

print "Entering reverse loop"
for r in reverseResults1 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)
					
### Typo loop 2 ###
print "There were " + str(len(skippedURLs)) + " skipped so far."
print "Entering vowel loop"
for r in vowelResults2 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)

print "Entering skip loop"
for r in skipResults2 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)	

print "Entering double loop"
for r in doubleResults2 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)	

print "Entering insert loop"
for r in insertResults2 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)		

print "Entering sub loop"
for r in subResults2 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)	

print "Entering reverse loop"
for r in reverseResults2 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)

### Typo loop 3 ###
print "There were " + str(len(skippedURLs)) + " skipped so far."
print "Entering vowel loop"
for r in vowelResults3 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)

print "Entering skip loop"
for r in skipResults3 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)	

print "Entering double loop"
for r in doubleResults3 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)	

print "Entering insert loop"
for r in insertResults3 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)		

print "Entering sub loop"
for r in subResults3 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)	

print "Entering reverse loop"
for r in reverseResults3 : 
	url = 'http://www.' + r
	url = stringAndStrip(url)
	for tld in tlds:
		tempURL = url + '.' + tld
		print 'Trying: ' + tempURL
		tryURL(tempURL)

### CORNER CASES ###
# The following looks for odd domains that I've noticed 

# This looks for 'teamfranklin'
url = 'http://www.team' + fName + '.com'
url = stringAndStrip(url)
print 'Trying: ' + url
tryURL(url)

url = 'http://www.team' + lName + '.com'
url = stringAndStrip(url)
print 'Trying: ' + url
tryURL(url)

url = 'http://www.team' + fName + lName + '.com'
url = stringAndStrip(url)
print 'Trying: ' + url
tryURL(url)

# This looks for 'repfranklin' 
# It's easier just to include for everyone, even if they are not in a congressional race
url = 'http://www.rep' + fName + '.com'
url = stringAndStrip(url)
print 'Trying: ' + url
tryURL(url)

url = 'http://www.rep' + lName + '.com'
url = stringAndStrip(url)
print 'Trying: ' + url
tryURL(url)

url = 'http://www.rep' + fName + lName + '.com'
url = stringAndStrip(url)
print 'Trying: ' + url
tryURL(url)

#These next few look for some of the larger parties
url = 'http://www.republican' + fName + lName + '.com'
url = stringAndStrip(url)
print 'Trying: ' + url
tryURL(url)

url = 'http://www.democrat' + fName + lName + '.com'
url = stringAndStrip(url)
print 'Trying: ' + url
tryURL(url)

url = 'http://www.libertarian' + fName + lName + '.com'
url = stringAndStrip(url)
print 'Trying: ' + url
tryURL(url)

url = 'http://www.independent' + fName + lName + '.com'
url = stringAndStrip(url)
print 'Trying: ' + url
tryURL(url)

# Wow! You've made it to the end. Well done! 

totalRuntime = time.time() - start_time, "seconds"

###### Write final results to logfile ###########
resultsFile.write("######################################" + "\n")
resultsFile.write("ElectionBuster v10 Scan Results: " + "\n")
resultsFile.write("######################################" + "\n")
resultsFile.write("INPUTS = " + str(fName) + ", " + str(lName) + ", " + str(year) + ", " + str(electionType) + str(state) + "\n") 
resultsFile.write("Total runtime was " + str(totalRuntime) + "\n")
resultsFile.write("There were " + str(len(confirmedURLs)) + " positive results." + "\n")
resultsFile.write("There were " + str(len(testedURLs)) + " unique URLs tested." + "\n")
resultsFile.write("-------------------------------------" + "\n")
resultsFile.write("Positive results: " + "\n")
resultsFile.write("-------------------------------------" + "\n")
for url in confirmedURLs:
	resultsFile.write(str(url) + "\n")
resultsFile.write("\n")
resultsFile.write("-------------------------------------" + "\n")
resultsFile.write("EOF " + "\n")
				
###### Print final results to screen ###########			
print "###################################### " + "\n"
print "ElectionBuster v10 Scan Results: " + "\n"
print "###################################### " + "\n"
print "INPUTS" + "\n"
print "First name: " + fName + "\n"
print "Last name: " + lName + "\n"
print "Year: " + year + "\n"
print "Election type: " + electionType + "\n"
print "-------------------------------------" + "\n"
print "Total runtime was " + str(totalRuntime) + "\n"
print "-------------------------------------" + "\n"
print "Positive results: " + "\n"
print "There were " + str(len(confirmedURLs)) + " hits:" + "\n"
print "-------------------------------------" + "\n"
for url in confirmedURLs:
	print url
print "\n"

#TODO: Parse goodResults.txt's pages and look for GoDaddy, Bluehost pages 
#TODO: Take screenshots

# Bad things happen if these files are not properly closed
resultsFile.close()
