import subprocess
import sys
import os
import re


p=os.system("nmcli d s > netname.txt")
with open("netname.txt") as f:			#get the name of first network device
	data = f.readlines()
	net= data[1]

keyword = 'connected'
info, keyword, netname = net.partition(keyword)
netname=netname.rstrip(" ")
netname=netname.lstrip(" ")
netname=netname.replace(" ","\\ ")
netname=netname[:len(netname)-3]


def getdns(): #get the current dns ip's
            p = os.system('nmcli dev show | grep DNS > dns.txt')

            with open("dns.txt") as f:
                data = f.read()
                dns= re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", data)
            return(dns)


def getip(): #get the machines ip

            process = subprocess.Popen(["hostname","-I"],stdout=subprocess.PIPE)

            out,err =process.communicate()

            out=out.strip()

            out=str(out)

            out=out.strip("b")

            out=out.strip("'")

            return(out)
ip=getip()
dns=getdns() #store inital dns's incase invalid dns passed
addrs=[]
for x in sys.argv[1:]:
            addrs.append(x)

print(dns,ip)
os.system("nmcli c m "+netname+" ipv4.method manual")  
os.system("nmcli c m "+netname+" ipv4.addresses "+ip)               
os.system("nmcli c m "+netname+" ipv4.dns '"+(" ").join(addrs)+"'")        #set to new dns
os.system("nmcli c m "+netname+" ipv4.gateway 10.100.49.254")              #set gateway
os.system("nmcli c down "+netname+" ") 
os.system("nmcli c up "+netname+" ")              # reset connection to update

presponse=os.system("ping -c 5 google.com")  #check if valid working dns

if presponse == 0:
	print("configuration ok!") 
else:
	print("Invalid ip address!")
	os.system("nmcli c m "+netname+" ipv4.method manual")
	os.system("nmcli c m "+netname+" ipv4.addresses "+ip)
	os.system("nmcli c m "+netname+" ipv4.gateway 10.100.49.254")                 
	os.system("nmcli c m "+netname+" ipv4.dns '"+(" ").join(dns)+"'")#if invalid revert dns to original
	os.system("nmcli c down "+netname+" ")
	os.system("nmcli c up "+netname+" ")





