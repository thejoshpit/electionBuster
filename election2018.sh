#!/bin/bash

#   ____   ___  _  ___    _____ _           _   _             
#  |___ \ / _ \/ |( _ )  | ____| | ___  ___| |_(_) ___  _ __  
#    __) | | | | |/ _ \  |  _| | |/ _ \/ __| __| |/ _ \| '_ \ 
#   / __/| |_| | | (_) | | |___| |  __/ (__| |_| | (_) | | | |
#  |_____|\___/|_|\___/  |_____|_|\___|\___|\__|_|\___/|_| |_|
                                                           
cd ~/electionbuster

d=`date +%Y%m%d`
mkdir -p $d
cd $d

for i in `cat ../candadites.txt | awk -F\, '{ print  "-f," $1 ",-l," $2 ",-y," $3 ",-e," $4 ",-s," $5  }'` 
	 do 	
		cmd=`echo $i | tr "," " "`  
		/home/kevin/electionbuster/Sbusterv17.py $cmd 
	done

