
# Trying to turn the data on its side (turn the data into a matrix we can work with easier)


function cmp_field(i1, v1, i2, v2) { 
	return i1 < i2 ? -1 : (i1 != i2)
}
{ 
	dates[$3] = 1; 
	sites[$2] = 1; 
	data[$2 ":" $3] = 1;
} 
END { 
	ORS = ","
	PROCINFO["sorted_in"] = "cmp_field"; 
	for ( d in dates ) {
		print d ;
	}
	print "site";
	printf "\n" ;
	for (s in sites) {  
		for ( d in dates ) {  
			data[s ":" d]++; 
			data[s ":" d]-- ;
			print data[s ":" d]  ;
		} 
		print s ; 
		printf "\n" ;
	}  
} 

