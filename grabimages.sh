#!/bin/bash

homed=/media/home/kevin/electionbuster

cd $homed

d=`date +%Y%m%d`

cd $d

for j in `ls result*.txt` 
do
	nohup env DISPLAY=:0 $homed/resultsScreen.sh $j &
done

