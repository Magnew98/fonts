import subprocess
import sys
import os


p=os.system("nmcli d s > netname.txt")


with open("netname.txt") as f:
	data = f.readlines()				#get the name of first network device
	net= data[1]

keyword = 'connected'
info, keyword, netname = net.partition(keyword)
netname=netname.rstrip(" ")
netname=netname.lstrip(" ")
netname=netname.replace(" ","\\ ")
netname=netname[:len(netname)-3]

os.system("nmcli c m "+netname+" ipv4.method auto") 
os.system("nmcli c down "+netname+" ") 
os.system("nmcli c up "+netname+" ")              # reset connection to update

