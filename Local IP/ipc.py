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


def getip(): #get the machines ip

            process = subprocess.Popen(["hostname","-I"],stdout=subprocess.PIPE)

            out,err =process.communicate()

            out=out.strip()

            out=str(out)

            out=out.strip("b")

            out=out.strip("'")

            return(out)

ip=getip() #store inital ip incase invalid ip passed

os.system("nmcli c m "+netname+" ipv4.method manual")                 
os.system("nmcli c m "+netname+" ipv4.addresses "+str(sys.argv[1]))        #set to new ip
os.system("nmcli c m "+netname+" ipv4.gateway 10.100.49.254")              #set gateway
os.system("nmcli c m "+netname+" ipv4.dns '8.8.8.8 172.29.0.50 192.168.181.16 '")   #set dns servers
os.system("nmcli c down "+netname+" ") 
os.system("nmcli c up "+netname+" ")              # reset connection to update

presponse=os.system("ping -c 5 google.com")  #check if valid working ip

if presponse == 0:
	print("configuration ok!") 
else:
	print("Invalid ip address!")
	os.system("nmcli c m "+netname+" ipv4.method manual")
	os.system("nmcli c m "+netname+" ipv4.addresses "+ip)
	os.system("nmcli c m "+netname+" ipv4.gateway 10.100.49.254")                 #if invalid revert ip to original
	os.system("nmcli c m "+netname+" ipv4.dns '172.29.0.50 192.168.181.16'")
	os.system("nmcli c down "+netname+" ")
	os.system("nmcli c up "+netname+" ")	




