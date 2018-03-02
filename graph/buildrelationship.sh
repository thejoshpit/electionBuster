#!/bin/bash

#
# Build the adjency matrix for the relationship graph
#

# Move to the given directory
cd $1

# Ensure no temp files or prev relationship files exist
rm -f *.tmp
rm -f temp.relationship
rm -f relationship.dat

# For each of the results files create a temp file that contains the relationships
for i in `ls results-*.txt` 
do
	ln=`echo $i | awk -F'-' '{print  $3}'`.tmp
	echo $i " -> " $ln
	grep -A 1 "Page Exist" $i | paste - - - > $ln
done

# Get the temp adjency matrix (its a bit hosed so we will have to reorder it in the next step)
grep Page *.tmp | sed -e 's/Page Exists://' | sed -e 's/http:\/\///'g | sed -e 's/https:\/\///'g | sed -e 's/.tmp://' | sed -e 's/\/\t/ /' | awk '{ print $1, $2, $3}' | tr -d ',$' | awk '{ print $2, $3, $1 }' > temp.relationship

# Reorder it so it is "from -> to" 
cat temp.relationship | awk '{ split($1, a1, "/"); split( $2, a2, "/"); if ( a1[1] != a2[1] ) printf "%s %s %s\n", a2[1], a1[1], $3 }' > relationship.dat

# Clean up the temporary files
rm -f *.tmp
rm -f temp.relationship

# Now we are left with the adjency matrix in the file relationship.dat
wc --lines relationship.dat
