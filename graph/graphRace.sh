#!/bin/bash 

# Where everything is run from 
EBHOME=~/electionbuster

cur=`pwd`
cd $1

tmpfile=/tmp/$$.tmp
# Build the tmpfile
for i in `ls *.txt` 
do 
	grep -h -A 1 "Page Exist" $i | paste - - - | sed -e "s/^/$i /"  
done | awk '{ print $1, $4, $5 }' | sed 's/,$/\//' > $tmpfile

# Get the date of the run
te=`pwd `
dte=`basename $te`

cd $cur

# Identify Strong relationships
$EBHOME/graph/find_strong.pl $tmpfile | sort | uniq > strong.txt

# Identify weaker relationships
$EBHOME/graph/find_weak.pl $tmpfile | sort | uniq > weak.txt

# We could graph both together in one go but this is simpler 
graphTitle="Potential Candidate Name Space Planting or Redirection"
$EBHOME/graph/network_graph.r -f strong.txt -t "$graphTitle" -d "$dte" -r $2
graphTitle="Potential Bad Faith Domain or Cyber Squatting"
$EBHOME/graph/network_graph.r -f weak.txt -t "$graphTitle" -d "$dte" -r $2

# Combine the pdf's into a single pdf
pdftk weak.txt.pdf strong.txt.pdf cat output t1.pdf
# Update some meta information
pdftk t1.pdf update_info $EBHOME/graph/PDFINFO1.TXT output t2.pdf
name=$2_
pdftk t2.pdf update_info $EBHOME/graph/PDFINFO2.TXT output $name$dte.pdf
echo "Output graph: $name$dte.pdf"
# Clean up
rm t1.pdf
rm t2.pdf
rm weak.txt.pdf 
rm strong.txt.pdf
#rm strong.txt
rm weak.txt
rm $tmpfile

