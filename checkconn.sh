#!/bin/bash

# I'm not sure this works properly but in the event it does this should reset
# the connection to the network (if its down) before running the election scripts

if [ $(nm-tool|grep State|cut -f2 -d' '| head -1) == "connected" ]; then
    echo "Connected"
else
    nmcli dev connect iface eth0
fi

