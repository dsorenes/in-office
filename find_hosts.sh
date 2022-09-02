#!/bin/bash

# nmap -sP 192.168.1.0/24 > /dev/null

# prints hostname and ip of devices connected to network
arp -a -i en0 | grep -E "^\w" | awk '{print $1, $2}'
