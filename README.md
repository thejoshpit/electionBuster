electionBuster.py
=================

This tool scans the URLs, and assocaited typos, of candidate election pages. This is done in an attempt to identitfy typosquatters. The time the tool takes to run is highly dependent on multiple factors, but the two most important factors seem to be length of the candidate's name (and state) and the type of network medium the tool is run over (i.e., wired or wireless). Wired connections often take about 30 minutes to an hour to complete, while wireless connections cause the program to finish in around 8 to 10 hours. 

Example types of candidate URLs it looks for are:

- joshfranklin.com
- josh2014.com
- franklin2014.com
- joshfranklin2014.com
- joshfranklinforDC.com
- joshfranklinDC.com
- joshforpresident.com
- josh4president.com
- joshforpresident2014.com
- josh4president2014.com
- presidentjoshfranklin.com
- president-josh-franklin.com
- presidentjoshforpresident2014.com
- presidentjosh4president2014.com
- presidentjoshfranklinforpresident2014.com
- presidentjosh-franklinforpresident2014.com
- presidentjoshfranklin4president2014.com
- presidentjosh-franklin4president2014.com

The tool prints output to the screen, but also writes to a logfile. The resulting logfiles are often ~3-5 MB. 

Problems:
- Middle names and middle inititals cause problems. The program cant only take in first names and last names as valid inputs. I typically googled the individual with a middle name/initial to see if it is actually used in their marketing material. If it is, I tend to concatenate it with the last name. 
- Special characters (non-english characters) cause the program problems. I tend to google the candidate and see how they dealing with this situation (e.g., changing an é to an e) and copy that. 

To do list:
- Add in support for small elections such as councilmember, ward, and sheriff
