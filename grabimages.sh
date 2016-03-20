#!/bin/bash

homed=/home/kevin/Desktop/nightly

cd $homed

d=`date +%Y%m%d`

cd $d

for j in `ls result*.txt` 
do
	$homed/resultsScreen.sh $j
done


