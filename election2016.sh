#!/bin/bash

cd /home/kevin/Desktop/nightly

d=`date +%Y%m%d`
mkdir $d
cd $d

../electionBuster.py -f Hillary -l CLinton -y 2016 -e President -s NY
../electionBuster.py -f Bernie -l Sanders -y 2016 -e President -s VT
../electionBuster.py -f Chris -l Christie -y 2016 -e President -s NJ
../electionBuster.py -f George -l Pataki -y 2016 -e President -s NY
../electionBuster.py -f Jeb -l Bush -y 2016 -e President -s FL
../electionBuster.py -f Ben -l Carson -y 2016 -e President -s MI
../electionBuster.py -f Ted -l Cruz -y 2016 -e President -s TX
../electionBuster.py -f Carly -l Fiorina -y 2016 -e President -s CA
../electionBuster.py -f Jim -l Gilmore -y 2016 -e President -s VA
../electionBuster.py -f Mike -l Huckabee -y 2016 -e President -s AK
../electionBuster.py -f John -l Kasich -y 2016 -e President -s OH
../electionBuster.py -f Rand -l Paul -y 2016 -e President -s KY
../electionBuster.py -f Marco -l Rubio -y 2016 -e President -s FL
../electionBuster.py -f Rick -l Santorum -y 2016 -e President -s PA
../electionBuster.py -f Donald -l Trump -y 2016 -e President -s NY
../electionBuster.py -f Lindsey -l Graham -y 2016 -e President -s SC
../electionBuster.py -f Bobby -l Jindal -y 2016 -e President -s LA
../electionBuster.py -f Rick -l Perry -y 2016 -e President -s TX
../electionBuster.py -f Scott -l Walker -y 2016 -e President -s WI
../electionBuster.py -f Martin -l OMalley -y 2016 -e President -s MD

