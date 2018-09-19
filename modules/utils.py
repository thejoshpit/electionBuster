#!/usr/bin/python3.5

import requests
import socket
from multiprocessing import Pool as ThreadPool, Manager

testedURLs = Manager().list()


def generate_urls(first_name, last_name, middlename=None, state=None, position=None, altPosition=None, year=None):

    templates = []
    fName = first_name.lower()
    lName = last_name.lower()
    shortYear = year[-2:]
    if middlename:
        mName = middlename.lower()
        middleInitial = mName[0]

    if state is not None:
        templates.append(fName + lName)
        templates.append(fName + '-' + lName)
        templates.append(lName + fName)
        templates.append(lName + '-' + fName)
        templates.append(fName + year)
        templates.append(fName + shortYear)
        templates.append(lName + year)
        templates.append(lName + shortYear)
        templates.append(fName + lName + year)
        templates.append(fName + lName + shortYear)
        templates.append(fName + '-' + lName + year)
        templates.append(fName + '-' + lName + shortYear)
        for stateAlias in state:
            templates.append(fName + lName + 'for' + stateAlias)
            templates.append(fName + lName + 'for' + stateAlias + year)
            templates.append(fName + lName + 'for' + stateAlias + shortYear)
            templates.append(lName + 'for' + stateAlias)
            templates.append(lName + 'for' + stateAlias + year)
            templates.append(lName + 'for' + stateAlias + shortYear)
            templates.append(fName + 'for' + stateAlias)
            templates.append(fName + 'for' + stateAlias + year)
            templates.append(fName + 'for' + stateAlias + shortYear)
            templates.append(fName + '-' + lName + 'for' + stateAlias)
            templates.append(fName + lName + '4' + stateAlias)
            templates.append(fName + '-' + lName + '4' + stateAlias)
            templates.append(fName + lName + stateAlias)
            templates.append(fName + '-' + lName + stateAlias)
        templates.append(fName + lName + 'for' + position)
        templates.append(fName + '-' + lName + 'for' + position)
        templates.append(fName + lName + '4' + position)
        templates.append(fName + '-' + lName + '4' + position)
        templates.append(fName + 'for' + position)
        templates.append(fName + '4' + position)
        templates.append(fName + 'for' + position + year)
        templates.append(fName + 'for' + position + shortYear)
        templates.append(fName + '4' + position + year)
        templates.append(fName + '4' + position + shortYear)
        templates.append(position + fName + lName)
        templates.append(position + '-' + fName + lName)
        templates.append(position + fName + '-' + lName)
        templates.append(position + '-' + fName + '-' + lName)
        templates.append(fName + lName + 'for' + altPosition)
        templates.append(fName + lName + '4' + altPosition)
        templates.append(fName + 'for' + altPosition)
        templates.append(fName + '4' + altPosition)
        templates.append(lName + 'for' + altPosition)
        templates.append(lName + 'for' + position)
        templates.append(lName + '4' + position)
    # This one is for middle name only
    if (middlename):
        templates.append(fName + lName)
        templates.append(fName + mName + lName)
        templates.append(fName + middleInitial + lName)
        templates.append(fName + '-' + lName)
        templates.append(lName + fName)
        templates.append(lName + '-' + fName)
        templates.append(fName + year)
        templates.append(lName + year)
        templates.append(fName + lName + year)
        templates.append(fName + '-' + lName + year)
        templates.append(fName + lName + 'for' + position)
        templates.append(fName + '-' + lName + 'for' + position)
        templates.append(fName + lName + '4' + position)
        templates.append(fName + '-' + lName + '4' + position)
        templates.append(fName + mName + 'for' + position)
        templates.append(fName + mName + year)
        templates.append(fName + middleInitial + year)
        templates.append(fName + mName + 'for' + position + year)
        templates.append(fName + middleInitial + 'for' + position + year)
        templates.append(fName + middleInitial + 'for' + position)
        templates.append(fName + 'for' + position)
        templates.append(fName + '4' + position)
        templates.append(fName + 'for' + position + year)
        templates.append(fName + '4' + position + year)
        templates.append(position + fName + lName)
        templates.append(position + '-' + fName + lName)
        templates.append(position + fName + '-' + lName)
        templates.append(position + '-' + fName + '-' + lName)
        templates.append(fName + lName + 'for' + altPosition)
        templates.append(fName + lName + '4' + altPosition)
        templates.append(fName + 'for' + altPosition)
        templates.append(fName + '4' + altPosition)
        templates.append(lName + 'for' + altPosition)
        templates.append(lName + 'for' + position)
        templates.append(lName + '4' + position)
    # This one is middle name and state
    if middlename and state:
        templates.append(fName + lName)
        templates.append(fName + mName + lName)
        templates.append(fName + middleInitial + lName)
        templates.append(fName + '-' + lName)
        templates.append(lName + fName)
        templates.append(lName + '-' + fName)
        templates.append(fName + year)
        templates.append(fName + shortYear)
        templates.append(lName + year)
        templates.append(lName + shortYear)
        templates.append(fName + lName + year)
        templates.append(fName + lName + shortYear)
        templates.append(fName + '-' + lName + year)
        templates.append(fName + '-' + lName + shortYear)
        for stateAlias in state:
            templates.append(fName + lName + 'for' + stateAlias)
            templates.append(fName + lName + 'for' + stateAlias + year)
            templates.append(fName + lName + 'for' + stateAlias + shortYear)
            templates.append(lName + 'for' + stateAlias)
            templates.append(lName + 'for' + stateAlias + year)
            templates.append(lName + 'for' + stateAlias + shortYear)
            templates.append(fName + '-' + lName + 'for' + stateAlias)
            templates.append(fName + lName + '4' + stateAlias)
            templates.append(fName + '-' + lName + '4' + stateAlias)
            templates.append(fName + lName + stateAlias)
            templates.append(fName + '-' + lName + stateAlias)
        templates.append(fName + lName + 'for' + position)
        templates.append(fName + '-' + lName + 'for' + position)
        templates.append(fName + lName + '4' + position)
        templates.append(fName + '-' + lName + '4' + position)
        templates.append(fName + mName + 'for' + position)
        templates.append(fName + mName + year)
        templates.append(fName + mName + shortYear)
        templates.append(fName + middleInitial + year)
        templates.append(fName + middleInitial + shortYear)
        templates.append(fName + mName + 'for' + position + year)
        templates.append(fName + mName + 'for' + position + shortYear)
        templates.append(fName + middleInitial + 'for' + position + year)
        templates.append(fName + middleInitial + 'for' + position + shortYear)
        templates.append(fName + middleInitial + 'for' + position)
        templates.append(fName + 'for' + position)
        templates.append(fName + '4' + position)
        templates.append(fName + 'for' + position + year)
        templates.append(fName + 'for' + position + shortYear)
        templates.append(fName + '4' + position + year)
        templates.append(fName + '4' + position + shortYear)
        templates.append(position + fName + lName)
        templates.append(position + '-' + fName + lName)
        templates.append(position + fName + '-' + lName)
        templates.append(position + '-' + fName + '-' + lName)
        templates.append(fName + lName + 'for' + altPosition)
        templates.append(fName + lName + '4' + altPosition)
        templates.append(fName + 'for' + altPosition)
        templates.append(fName + '4' + altPosition)
        templates.append(lName + 'for' + altPosition)
        templates.append(lName + 'for' + position)
        templates.append(lName + '4' + position)
    # this one is the least number of parameters, just the basics
    templates.append(fName + lName)
    templates.append(fName + '-' + lName)
    templates.append(lName + fName)
    templates.append(lName + '-' + fName)
    templates.append(fName + year)
    templates.append(fName + shortYear)
    templates.append(lName + year)
    templates.append(lName + shortYear)
    templates.append(fName + lName + year)
    templates.append(fName + lName + shortYear)
    templates.append(fName + '-' + lName + year)
    templates.append(fName + '-' + lName + shortYear)
    templates.append(fName + lName + 'for' + position)
    templates.append(fName + '-' + lName + 'for' + position)
    templates.append(fName + lName + '4' + position)
    templates.append(fName + '-' + lName + '4' + position)
    templates.append(fName + 'for' + position)
    templates.append(fName + '4' + position)
    templates.append(fName + 'for' + position + year)
    templates.append(fName + 'for' + position + shortYear)
    templates.append(fName + '4' + position + year)
    templates.append(fName + '4' + position + shortYear)
    templates.append(fName + 'for' + position + year)
    templates.append(lName + 'for' + position + shortYear)
    templates.append(lName + '4' + position + year)
    templates.append(lName + '4' + position + shortYear)
    templates.append(position + fName + lName)
    templates.append(position + '-' + fName + lName)
    templates.append(position + fName + '-' + lName)
    templates.append('vote' + fName)
    templates.append('vote' + lName)
    templates.append('votefor' + fName)
    templates.append('votefor' + lName)
    templates.append('votefor' + fName + lName)
    templates.append('vote4' + fName)
    templates.append('vote4' + lName)
    templates.append('vote4' + fName + lName)
    templates.append(position + '-' + fName + '-' + lName)
    templates.append(fName + lName + 'for' + altPosition)
    templates.append(fName + lName + '4' + altPosition)
    templates.append(fName + 'for' + altPosition)
    templates.append(fName + '4' + altPosition)
    templates.append(lName + 'for' + altPosition)
    templates.append(lName + 'for' + position)
    templates.append(lName + '4' + position)

    return templates



def gen(website_name, alt_alphabet):
    A = 'abcdefghijklmnopqrstuvwxyz1234567890'  # original alphabet string
    xform = str.maketrans(A, alt_alphabet)
    s = website_name.translate(xform)
    return s

def genAll(website_names, alphabets):
    results = []
    for s in website_names:
        for a in alphabets:
            mangled_name = gen(s, a)
            results.append(mangled_name)
    return results

def genAllDonate(website_names, alphabets):
    results = []
    for s in website_names:
        for a in alphabets:
            mangled_name = gen(s, a)
            results.append( mangled_name + 'donate' )
    return results





def tryURLforReal(url):
    fetchResult = ""
    global confirmedURLs, testedURLs
    if url not in testedURLs:
        testedURLs.append(url)
        try:
            # Open input URL
            httpResponse = requests.get(url, timeout=10)
            fetchResult = "*************************************************+" + "\n"
            fetchResult = fetchResult + "Page Exists: " + httpResponse.url + "\n"
            fetchResult = fetchResult + str(url) + ", " + str(httpResponse.status_code) + "\n"
            fetchResult = fetchResult + str(httpResponse.headers) + "\n"
            fetchResult = fetchResult + "*************************************************+" + "\n"
            print(fetchResult)
            confirmedURLs.append(url)

            return fetchResult
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            pass
        except socket.timeout as e:
            pass
    return fetchResult


