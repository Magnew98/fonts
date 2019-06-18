import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from board import SCL, SDA
import busio
import adafruit_ssd1306
import ip_changer
import dns
SPI_PORT   = 0
SPI_DEVICE = 0
stick = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
import time
lis=[]
def main():
	global lis
	options=["Static" ,"Dynamic"]
	disp.fill(0)
	disp.text("-- "+options[0]+" --",27,10,1)
	disp.text(options[1],45,20,1)
	disp.show()
	screen=10
	a=1
	while True:
		if stick.read_adc(2) < 90:
			time.sleep(0.4)
			if screen == 10:
				a = 1
				disp.fill(0)
				disp.text("-- "+options[0]+" --",27,10,1)
				disp.text(options[1],45,20,1)
				disp.show()


			if screen == 1 and a == 5 :
  
				lis=[1]
				print(a) 
				disp.fill(0)
				disp.text("Set Ip",45,10,1)
				disp.text("-- "+"Set Dns"+" --",27,20,1)
				disp.text("<-",0,25,1)
				disp.show()

				print(lis)
				a=6
			elif screen == 1:
				lis=[]
				disp.fill(0)
				disp.text("Set Dns",45,20,1)
				disp.text("-- "+"Set Ip"+" --",27,10,1)
				disp.text("<-",0,25,1)
				disp.show()
				a=3
	
		                


		                

	 
		if stick.read_adc(2) > 700 :
			time.sleep(0.4)
			if screen == 10	:
				a=0		
				disp.fill(0)
				disp.text(options[0],45,10,1)
				disp.text("-- "+options[1]+" --",27,20,1)
				disp.show()
		
			elif screen == 1 and a !=5:
				disp.fill(0)
				disp.text("Set Ip",45,10,1)
				disp.text("-- "+"Set Dns"+" --",27,20,1)
				disp.text("<-",0,25,1)
				disp.show()
				lis.append(stick.read_adc(2))
				print(lis)
				a=4
			if screen == 1 and a == 4 and len(lis) > 1:
				disp.fill(0)
				disp.text("Set Ip",45,10,1)
				disp.text("Set Dns",45,20,1)
				disp.text("[ <- ]",0,25,1)
				a=5 
				disp.show()

				

		            
	
		if stick.read_adc(0) == 0:
			if a == 1:

		
				disp.fill(0)
				disp.text("Set Dns",45,20,1)
				disp.text("-- "+"Set Ip"+" --",27,10,1)
				disp.text("<-",0,25,1)
				disp.show()
				screen=1
	
	

			if a ==3:
				ip_changer.main()
			if a ==0:
				ip_changer.dynamic()
				disp.fill(0)
				disp.show()
				disp.text("Ip is now dynamic",0,0,1)
				disp.show()
				time.sleep(1)
				main()
			if a == 4:
				dns.main()
			if a == 5:
				time.sleep(0.4)
				main()
				
	

if __name__ == "__main__":
	main()

