electionBuster.py
=================

This tool scans the URLs, and assocaited typos, of candidate election pages. This is done in an attempt to identitfy for typosquatters. The time the tool takes to run is dependent on multiple factors, but the two most important factors seem to be length of the candidate's name (and state) and the type of network medium the tool is run over (i.e., wired or wireless). Wired connections often take about 30 minutes to an hour to complete, while wireless connections cause the program to finish in around 8 to 10 hours. 

Example types of candidate URLs it looks for are:

###http://www.joshfranklin.com
#*http://www.josh2014.com
*http://www.franklin2014.com
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

The tool prints output to the screen, but also writes to a logfile. The resulting logfiles are often ~3-5 MB. 
