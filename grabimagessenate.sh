#!/bin/bash

homed=/media/home/kevin/electionbuster

cd $homed/$1

d=`date +%Y%m%d`

cd $d

for j in `ls result*.txt` 
do
	pwd
	env DISPLAY=:0 $homed/resultsScreenSenate.sh $1 $j &
	outf=`basename $j .txt`
        $homed/getips.sh $j > $outf.ip

done

mkdir ~/git2/electionBuster/senate/$d
cp *.ip ~/git2/electionBuster/senate/$d
cd ~/git2/electionBuster/
git add senate/$d
git commit -m "ElectionBuster results $d" senate/$d
git push origin master 

