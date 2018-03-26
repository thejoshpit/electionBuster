electionBuster.py
=================
Electoral candidates from both sides of the aisle increasingly rely on the internet to promote their brands and to focus the message of their political platforms. Yet cyberspace isn’t safespace. How do voters know they’re viewing a candidate’s real website? How can voters ensure their online donations are actually going to a specific candidate or cause? Election cybercrime is a burgeoning area but little data exists on the size and scope of these unscrupulous activities. Election Buster is an open source suite of tools to begin to measure the scope of this problem and used it to scan every single candidate running for the house and senate (1000+ candidates)in the 2014 General Elections. We're continuing development and using it to scan the 2016 election.

This tool scans the URLs, and assocaited typos, of candidate election pages. This is done in an attempt to identitfy typosquatters. The time the tool takes to run is highly dependent on multiple factors, but the two most important factors are  length of the candidate's name (and state) and the type of network medium the tool is run over (i.e., wired or wireless). Wired connections often take about 30 minutes to an hour to complete, while wireless connections cause the program to finish in around 8 to 10 hours. 

Visit https://jfranklin.me/ElectionCybercrime for updates
Visit the following site for a slidedeck about a 2015 update on the project. 
http://jfranklin.me/prez/ElectionCybercrime-BsidesDC2015.pdf

Example types of candidate URLs it looks for are:

- joshfranklin.com
- josh2014.com
- franklin2014.com
- joshfranklin2014.com
- joshforpresident.com
- josh4president.com
- president-josh-franklin.com
- presidentjoshfranklin4president2014.com
- presidentjosh-franklin4president2014.com

The tool prints output to the screen, but also writes to a logfile. The resulting logfiles are often ~3-5 MB. 

2018 ToDo List  

We are moving to multiple versions 
- Election Buster: For scanning candidates 
- Election Aperture: For scanning Super PACs, campaign organizations (e.g., DNC), and state election portals (online voter registration systems and online ballot marking sites fun by state and local agencies)
- Post Processing script to highlight which sites need human review
- - remove parked domains 
- - Include number of URLs that were searched 
- - Compare IP addresses of hosted domains  

2016 Results Review 
- graph of pages per candidate each month 
- stuff like that 
- Need graph daigrams showing connections between domains 

2018 Election Buster TODOs: 
- New Domains: .ru, .cn, .link, .io, .pk, .pl, .top (COMPLETE: Kevin) 
- IP address capture (COMPLETE: Kevin)   
- HTML capture (COMPLETE: Kevin ) 
- Update WhoIs capture and storage (COMPLETE: Kevin - the tool WhoAreThey.py is deprecated)
- Include optional support for middle names (COMPLETE: Josh ) 
- Figure out when domains were first registered 
- Compare IP addresses of hosted domains
- Possibly embed IP address and whois info into the picture 
- Parse goodResults.txt's pages and look for GoDaddy, Bluehost pages 
- Log 300 and 400 series response codes as hits and log them (these are in the raw output of electionbuster)  (COMPLETE: Kevin added to result of getips.sh)
- Add in support for small elections such as councilmember, ward, and sheriff, or just a * field
- Change runtime to seconds. 
- Include party name as an optional input to note in the filename whether someone's a D or an R (COMPLETE: Kevin)
- Store 2018 logfiles on github (COMPLETE: Kevin)
- similar to page exists URL, have page not exists URL 

Known problems:
- Special characters (non-english characters) cause the program problems. I tend to google the candidate and see how they dealing with this situation (e.g., changing an é to an e) and copy that. 
- The number of hits the tool finds for a candidate is having a confusing scoping issue and doesn't function properly 

Exploring new areas

Explore the use of machine learning for site identification: 
- PhishZoo: Detecting Phishing Websites by Looking at Them
http://ieeexplore.ieee.org/document/6061361/

-At DEFCON last year, folks were finding sensitive election documentation online. Anyway to use a Google API to look for this stuff? 


Found a few more patterns
ELECTfirstlast.com      https://www.electmarciamorgan.com/
lastname4SENATE         http://www.stokes4senate.com/
firstmiddleyear.com     http://paulajean2018.com
MIDDLELAST.com          http://rikkivaughn.com/
	
