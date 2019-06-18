import menu
import ip_changer
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
a=0
i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
ip=[1,9,2,1,6,8,1,8,1,0,1,6]
iplist=[]
i=1
j=0
screen = 0
def change_dns(l):
    cs=""
    for p in l:
        cs+=p+" "
    p=os.system("sudo rm nohup.out")
    p=os.system("sudo nohup python3 dnsc.py "+p)
    time.sleep(5.8)
	with open("nohup.out") as f:
		data = f.readlines()
    c=data
    y = (str(c[-1].rstrip("\n").rstrip(" ")))
    b= 'configuration ok!'
    print(y[0:-1],b[0:],y[0:-1]==b)
    if y[0:-1] == b:
        disp.fill(0)
        disp.text("Dns has been set",0,0,1)
        disp.show()
        time.sleep(1)
    else:

        disp.fill(0)
        disp.text("Invalid Ip!",0,0,1)
        disp.show()
        time.sleep(1)




def main():
 global ip
 a=0
 time.sleep(0.8)
 disp.fill(0)
 disp.text("0",0,0,1)
 disp.show()
 global screen 
 while True:
            time.sleep(.08)
            global i
            global j
            global iplist
            if screen == 1:
               disp.fill(0)
               ip_changer.show_ip(ip,a,disp)
               disp.show()
            if stick.read_adc(2) < 90:
                      if screen == 0 and j < 3 :
                               j+=1                               
                               disp.fill(0)
                               disp.text(str(j),0,0,1)
                               disp.show()   
                      elif screen == 1:
                              if ip[a]+1==10:

                                    ip[a]=0

                                    
                                    print(ip_changer.ppip(ip))

                              else:    

                                    ip[a] = ip[a]+1
                     
                                   
                                    print(ip_changer.ppip(ip))

 

            if stick.read_adc(2) > 700 :
                      if screen == 0 and j > 0:
                         j-=1
                         disp.fill(0)
                         disp.text(str(j),0,0,1)
                         
                         disp.show() 
                      elif screen == 1:            

                           if ip[a]==0:
  
                                     ip[a]=9

                                     print(ip_changer.ppip(ip))

                           else:

                                    ip[a] = ip[a]-1
                                    print(ip_changer.ppip(ip))

 

            if stick.read_adc(1) > 700:
                       


                        if screen == 1:
                            if a+1 in range(0,len(ip)):                   

                                    a=a+1

 

            if stick.read_adc(1) < 90:

                        if screen == 1:                        
                           if a-1 in range(0,len(ip)):                                            

                                    a=a-1

            if stick.read_adc(0) == 0:
                        time.sleep(0.5)
                        print(screen)

                     
                        if screen == 1:
                            if  i <= j:
                               if ip != [0,0,0,0,0,0,0,0,0,0,0,0]:
                                         ip=ip_changer.ppip(ip)
                                         ip = (ip_changer.ipsplitter(ip))
                                         formated_ip= []
                                         for x in range(0,len(ip)):
                                                x="".join(ip[x]).lstrip("0")
                                                if x == "":
                                                        x="0"
                                                formated_ip.append(x)
                                         ip=".".join(formated_ip)

                                    
                                         iplist.append(ip)
                                         ip=[0,0,0,0,0,0,0,0,0,0,0,0]
                                         i+=1
                                         a=0
                               change_dns(iplist)
                               

                               #main()

                        
                            if i >=j:  
                              print(iplist)
                              iplist=[]
                              i=1
                              j=0
                              screen = 0
                              menu.main()
                              break
                        else:
                             screen = 1
                             disp.fill(0)
                             ip_changer.show_ip(ip,a,disp)
                             disp.show()


            
    
