#!/bin/bash

homed=/media/home/kevin/electionbuster

cd $homed

d=`date +%Y%m%d`

cd $d

for j in `ls result*.txt` 
do
	nohup env DISPLAY=:0 $homed/resultsScreen.sh $j &
	outf=`basename $j .txt`
	$homed/getips.sh $j > $outf.ip
done

mkdir ~/git2/electionBuster/president/$d
cp *.ip ~/git2/electionBuster/president/$d


$homed/graph/graphRace.sh . President
cp *.pdf ~/git2/electionBuster/president/$d

cd ~/git2/electionBuster/
git add president/$d
git commit -m "ElectionBuster results $d" president/$d
git push origin master 

