#!/usr/bin/env python

#################################
#	Ping Sweepr          #
#	A script to          #
#	Sweep your pings     #
#################################
from icmplib import ping
import sys
from time import sleep
import ipaddress 
from colorama import Fore, Style
cl_rd = Fore.RED
cl_gr = Fore.GREEN
cl_cy = Fore.CYAN
cl_mg = Fore.MAGENTA
cl_reset = Style.RESET_ALL

HELP_MESSAGE='''
swee-ping [RANGE] [COUNT] [INTERVAL]\n\nPositional Arguments (required):\n	ARG		FORMAT			DESCRIPTION\n----------------------------------------------------------------------------------
\n	RANGE:		192.168.1.1-255		Range on the subnet to scan\n			10.10.10.0/24		(only works with /24 ath the moment)\n			172.16.1.1		(single host)\n
\n	COUNT:		5			Number of times to probe each host\n\n	INTERVAL:	4			Interval between packets sent\n							(in seconds)\n\n	**  use -h or --help for to print this help message! **
\n----------------------------------------------------------------------------------\n\n\nExample:\npython3 swee-ping 192.168.1.1-100 1 2
'''

try:
    sys.argv[1]
except IndexError:
    print("USAGE: swee-ping RANGE COUNT INTERVAL\n\nUse -h or --help for help")
    exit(1)
if sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print(HELP_MESSAGE)
    exit(1)
try:
    address_range       = sys.argv[1]
    echo_count          = sys.argv[2]
    delay_interval      = sys.argv[3]
except:
    print(HELP_MESSAGE + "\nMUST PROVIDE ALL THREE ARGUMENTS!!!!")
    sys.exit(1)


def check_range_format(address_range):
    split_octets = address_range.split('.')
    last_octet = split_octets[3]
    if '-' in last_octet:
        return 'dash_range'
    elif '/' in last_octet:
        return 'cidr_block'
    else:
        print(cl_rd+"HOST MUST BE A RANGE!:\n"+cl_cy+"Please"+cl_reset+" use a dash range, or CIDR block!")
        exit()

def cidr_to_list(cidr_block):
    address_list = [str(ip) for ip in ipaddress.IPv4Network(cidr_block)]
    return address_list

def dash_to_list(address_range):
    address_list = []
    a = address_range.split('.')
    b = a[3]
    c = '.'.join(a[0:3])
    d = b.split('-')
    e = int(d[0])
    f = int(d[1]) + 1
    for i in range(e,f):
        g = str(c)+'.'+str(i)
        address_list.append(g)
    return address_list

def scan_network(ip, cnt, intv):
    host = ping(ip, count=cnt, interval=intv)
    host_data = [host.address, host.is_alive]
    print("\ttryiing:\t{}".format(host.address))
    host_scan_data.append(host_data)

def scan_output_comments(address, host_state):
    if host_state:
        print(cl_cy+"\tStatus on "+cl_mg+"{}:".format(address) +cl_cy+" WE'VE GOT A LIVE ONE!" +cl_gr+"\t:D"+cl_reset)
    else:
        print(cl_rd+"\tStatus on {}: HE'S DEAD JIM".format(address) +cl_mg+"\t\tX_x"+cl_reset)

host_scan_data = []

reprot_template = ""

if check_range_format(address_range) == 'dash_range':
    to_scan = dash_to_list(address_range)

elif check_range_format(address_range) == 'cidr_block':
    to_scan = cidr_to_list(address_range)
else:
    to_scan = address_range

for i in range(len(to_scan)):
    scan_network(to_scan[i], int(echo_count), int(delay_interval))

for i in range(len(host_scan_data)):
    report = host_scan_data[i]

print(cl_gr+"\n\n\t\t###REPORT###"+cl_reset)
for i in range(len(host_scan_data)):
    status = host_scan_data[i][1]
    address = host_scan_data[i][0]
    scan_output_comments(address, status)

exit()
