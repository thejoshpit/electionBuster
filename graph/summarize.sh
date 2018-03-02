cd $1 > /dev/null

# Count the number of possible hits from the ElectionBuster output
for filename in `ls *.txt | sort` 
do
	cut1=`echo $filename | cut -b9-100 ` 
	cut2=`basename $cut1 .txt`
	name=`echo ${cut2:0:-11}`

	dateofit=`echo $cut2 | tail -c 11`

	count=`grep ", 200" $filename | sort | uniq | wc -l ` 
	printf "%-30s %s %4d\n" $name $dateofit $count

done
cd - > /dev/null
