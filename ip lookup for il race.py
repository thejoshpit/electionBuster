# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 20:21:18 2018

@author: iweinsto
"""
from bs4 import BeautifulSoup
from urllib import request
import pandas as pd

df = pd.read_excel('c:/users/iweinsto/documents/personal/election buster/403 Codes IL.xlsx')
base = 'https://tools.keycdn.com/geo?host='
urls = list(df.IP)
ip_df = pd.DataFrame()
for url in urls:
    r = request.urlopen(base+url).read()
    soup = BeautifulSoup(r,'lxml')
    data = soup.find_all('td')
    data_text = [s.get_text() for s in data]
    d = pd.DataFrame({'IP':[url],'Provider': [data_text[4]], 'Country':[data_text[3].lstrip(' ')], 'Region':[data_text[9]]})
    ip_df = ip_df.append(d)
deduped = ip_df.drop_duplicates(subset = 'IP')
new = pd.merge(left = df, right = deduped, how ='left', on = 'IP')
new.to_csv('c:/users/iweinsto/documents/personal/election buster/IPs with Data.csv', index = False)

everything = pd.read_csv('c:/users/iweinsto/documents/personal/election buster/IL Primary ROUGH.csv')
everything = everything.drop(['Candidate', 'State', 'Party', '2'], axis =1)
ips = []
nos = '0123456789'
for i in range(len(everything.columns.values)):
    for j in range(len(everything)):
        if (str(everything.ix[j,i]).count('.') == 3) & (str(everything.ix[j,i])[0] in nos):
            ips.append(everything.ix[j,i])

urls = list(set(ips))
ip_df = pd.DataFrame()
for url in urls:
    r = request.urlopen(base+url).read()
    soup = BeautifulSoup(r,'lxml')
    data = soup.find_all('td')
    data_text = [s.get_text() for s in data]
    d = pd.DataFrame({'IP':[url],'Provider': [data_text[4]], 'Country':[data_text[3].lstrip(' ')], 'Region':[data_text[9]]})
    ip_df = ip_df.append(d)
ip_df.to_csv('c:/users/iweinsto/documents/personal/election buster/All IPs with Data.csv', index = False)
