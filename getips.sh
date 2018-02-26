#!/bin/bash


resultfile=$1
procid=$$
tmpfile=/tmp/$procid.txt

grep -A 1 "Page Exist" $resultfile  | paste - - - | awk '{ print $3, $4, $5}' | sed 's/,$//' > $tmpfile
echo $tmpfile
while read j
do
	arg1=`echo $j | awk '{ print $1}'`
	arg1d=`echo "$arg1" | awk -F/ '{print $3}'`
	argresp=`echo "$j" | awk '{print $3}'`
	arg1ip=`dig +short $arg1d`

	arg2=`echo $j | awk '{ print $2}' | tr -d ', '`
	arg2d=`echo "$arg2" | awk -F/ '{print $3}'`
	arg2ip=`dig +short $arg2d | tail -1`
	echo $arg2 $argresp $arg1 $arg1ip | tr ' ' ','
done <$tmpfile

rm $tmpfile


