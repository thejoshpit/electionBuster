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
- Sometimes the code exits right before the results are written, after the scan has occured. 

To do list:
- Add in support for small elections such as councilmember, ward, and sheriff, or just a * field
- Include optional support for middle names
- Change runtime to seconds. 
- Log 300 and 400 series response codes as hits and log them
