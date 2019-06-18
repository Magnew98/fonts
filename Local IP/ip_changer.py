#! /bin/sh

import menu
import subprocess
import re
import os
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from board import SCL, SDA
import busio
import adafruit_ssd1306

SPI_PORT   = 0
SPI_DEVICE = 0
stick = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
disp.fill(0)
disp.show()

ip_used=[]

#Have to find a way to send the subprocess call to change ip to the COB/system and not have to enter pass for sudo manually
x=0

def change_ip(ip):   #set new ip address to the one entered
	global ip_used
	l=[]
	i=0                      
	ip=ppip(ip)
	ip = (ipsplitter(ip))
	formated_ip= []
	for i in range(0,len(ip)):
		i="".join(ip[i]).lstrip("0")
		if i == "":
			i="0"
		formated_ip.append(i)

	ip=".".join(formated_ip)
	print(ip_used)
	if ip in ip_used:
		disp.fill(0)
		disp.show()
		disp.text("IP in use already!",0,8,1)
		disp.text("try again.",0,16,1)
		disp.show()
		main()
	else:
		p=os.system("sudo nohup python3 ipc.py "+ip)
		time.sleep(1)
		print(ip)
            
            

def dynamic() :
	p=os.system("sudo nohup python3 setdyn.py")
	time.sleep(1)

	
 

def ppip(ip): #pretty print the ip adress
	p=ip[:]
	x=0
	for i in p:
		p[x] = str(i)
		x+=1
	p="".join(p)
	p=".".join([(p[i:i+3]) for i in range(0,len(p),3)])
	return p

 

def prepip(): #prepare the ip for being edited
	return(padip(ipsplitter(getip())))

def getip(): #get the machines ip
	p = subprocess.Popen(["sudo nmap -nsP 10.100.49.0/24 | grep -B2 08:00:27:D6:D0:72"],shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout,stderr = p.communicate()
	i =str(stdout).split("\\n")
	i=i[0].split(" ")
	i=i[-1]
	return(i)


def ipsplitter(ip): #split ip (eg. 10.0.2.15) in the format of [['1', '0'], ['0'], ['2'], ['1', '5']]
	ip=ip.split(".")
	sip=[]
	for i in ip:
		i=i.split()
		sip.append(i)
	ip = []
	for i in sip:
		for j in i:
			j=list(j)
			ip.append(j)
	return(ip)

           

def padip(iplist):   #buffs out split ip to look like [['0','1', '0'], ['0','0','0'], ['0','0','2'], ['0','1', '5']]
	for i in iplist:
		x=0
		if len(i) != 3:
			while x<=3-len(i):
				i.insert(0,"0")
				x+=1
	return iplist

def joinip(ip): #rejoin ip together
	i=0
	for j in ip:
		if len(j) >1 :
			ip[i]="".join(j)
		else:
			ip[i]=j[0]
		i+=1
	return("".join(ip))

def show_ip(ip,a,disp):
	global x
	b=a
	if b >= 3 and b < 6:
		b=b+1
	elif b >= 6 and b < 9:
		b=b+2
	elif b >= 9:
		b=b+3
	if x==0:
		disp.text(ppip(ip),0,10,1)
		x+=1
	else:
		disp.text(ppip(ip)[:b]+" "+ppip(ip)[b+1:],0,10,1)
		x-=1 

                       


def main():
	try:
		global ip_used
		p = os.system('sudo nmap -nsP 10.100.49.0/24 > nets.txt')
		with open("nets.txt") as f:
			data = f.read()
		ip_used = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", data)
		ip = prepip()
		ip= joinip(ip)
		ip=[int(i) for i in ip]     
		a=0
		disp.fill(0)
		disp.text(ppip(ip),0,10,1)
		disp.show()
		while True:
			time.sleep(.08)
			disp.fill(0)
			show_ip(ip,a,disp)
			disp.show()
			if stick.read_adc(2) < 90:
				if ip[a]+1==10:
					ip[a]=0
					print(ppip(ip))

				else:    
					ip[a] = ip[a]+1
					print(ppip(ip))
			if stick.read_adc(2) > 700 :
				if ip[a]==0:
					ip[a]=9
					print(ppip(ip))
				else:
					ip[a] = ip[a]-1
					print(ppip(ip))
			if stick.read_adc(1) > 700:
				if a+1 in range(0,len(ip)):                   
					a=a+1
			if stick.read_adc(1) < 90:
				if a-1 in range(0,len(ip)):                                            
					a=a-1
			if stick.read_adc(0) == 0:
				change_ip(ip)
				break
		    

		ip=ppip(ip)
		ip = (ipsplitter(ip))
		formated_ip= []
		for i in range(0,len(ip)):
			i="".join(ip[i]).lstrip("0")
			if i == "":
				i="0"
			formated_ip.append(i)
		ip=".".join(formated_ip)
		print("The ip adress has been set to:",ip)
		disp.fill(0)
		disp.show()
		disp.text("The ip adress has",0,0,1)
		disp.text("been set to: ",0,8,1)
		disp.text(ip,0,16,1)
		disp.show()
		time.sleep(10)
		menu.main()
	except Exception as e :
		disp.fill(0)
		disp.show()
		disp.text("Error! ",0,0,1)
		disp.text("program restarting!",0,8,1)
		disp.text("try again.",0,16,1)
		disp.show()
		print(str(e))    
		main()



if __name__ == "__main__":
    main()
