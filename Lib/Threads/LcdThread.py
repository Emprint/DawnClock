# -*- coding: utf-8 -*-
from ..Adafruit.LCD.Adafruit_CharLCD import Adafruit_CharLCD
from ..Adafruit.LCD.Adafruit_MCP230xx import MCP230XX_GPIO
import time
import threading

class LcdThread(threading.Thread):

	def __init__(self, main, shutdownCallback):
		threading.Thread.__init__(self)
		self.main = main
		self.stopping = False
		self.bus = 1         # Note you need to change the bus number to 0 if running on a revision 1 Raspberry Pi.
		self.address = 0x20  # I2C address of the MCP230xx chip.
		self.gpio_count = 8  # Number of GPIOs exposed by the MCP230xx chip, should be 8 or 16 depending on chip.

		# Create MCP230xx GPIO adapter.
		self.mcp = MCP230XX_GPIO(self.bus, self.address, self.gpio_count)
		
		# Create LCD, passing in MCP GPIO adapter.
		self.lcd = Adafruit_CharLCD(pin_rs=1, pin_e=2, pins_db=[3,4,5,6], GPIO=self.mcp, pin_b=7)
		self.lcd.begin(16, 2)
		self.lcd.backlight(True)
		#self.registerCustomChars() #Call it once
		self.clear()
		self.execute()
		
		
	def stop(self):
		self.main.log("LCD Shutting down")
		self.center("Shutting down", 0, True)
		time.sleep(1)
		self.clear()
		self.lcd.backlight(False)
		self.stopping=True
		
	
	def setCursor(self, col = 0, line = 0):
		self.lcd.setCursor(col, line)
		
	
	def message(self, text, clear = True):
		if clear:
			self.clear()
			
		self.lcd.message(text)
		
		
	def center(self, text, line = 0, clear = False):
		if clear:
			self.clear()
		self.setCursor(0, line)
		self.message(text.center(16), False)
		
	
	def clear(self):
		self.lcd.clear()
		
	#https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=28915
	def registerCustomChar(self, addr, bytes):
		self.lcd.write4bits(self.lcd.LCD_SETCGRAMADDR + addr*8)
		for b in bytes:
			self.lcd.write4bits(b, True)
		time.sleep(0.1)
	
	#Generate using this template http://www.quinapalus.com/hd44780udg.html
	#Can store up to 8 custom chars	
	def registerCustomChars(self):
		eacute = [0x2,0x4,0xe,0x11,0x1f,0x10,0xe] 	#\x00 or chr(0)
		egrave = [0x8,0x4,0xe,0x11,0x1f,0x10,0xe] 	#\x01 or chr(1)
		ecirc = [0x4,0xa,0xe,0x11,0x1f,0x10,0xe] 	#\x02 or chr(2)
		aacute = [0x8,0x4,0xe,0x1,0xf,0x19,0xf] 	#\x03 or chr(3)
		acirc = [0x4,0xa,0xe,0x1,0xf,0x19,0xf] 		#\x04 or chr(4)
		ugrave = [0x8,0x4,0x11,0x11,0x11,0x13,0xd] 	#\x05 or chr(5)
		
		chars = [eacute, egrave, ecirc, aacute, acirc, ugrave]
		addr = 0
		for char in chars:
			self.registerCustomChar(addr, char)
			addr += 1
	
	def testChars(self):
		self.clear()
		for char in range(0, 256):
			self.setCursor(0, 0)
			self.message(str(char) + ' : ' + chr(char), False)
			time.sleep(.5)
		
		
	def execute(self):
		self.main.log("LCD Starting")
		self.center("Hello, Bonjour !")
		self.center("D\x00marrage", 1)
		time.sleep(1)
		
		#self.setCursor(0, 1)
		#self.message("awnClock démarre", False)
		#time.sleep(1)
		
		self.center("DawnClock", 1, True)
		
		#time.sleep(1)
		#self.testChars()
		
		

		try:
			while(not self.stopping):
				time.sleep(0.1)
				
		except (KeyboardInterrupt, SystemExit):
		#	self.stop()
			self.main.stop()
				
		except:
			self.main.log("Error in LcdThread loop")
			self.main.stop()
				