#!/usr/bin/python
# Example script to show usage of MCP230xx GPIO extender to drive character LCD.
from Adafruit.LCD.Adafruit_CharLCD import Adafruit_CharLCD
from Adafruit.LCD.Adafruit_MCP230xx import MCP230XX_GPIO
import time

bus = 1         # Note you need to change the bus number to 0 if running on a revision 1 Raspberry Pi.
address = 0x20  # I2C address of the MCP230xx chip.
gpio_count = 8  # Number of GPIOs exposed by the MCP230xx chip, should be 8 or 16 depending on chip.

# Create MCP230xx GPIO adapter.
mcp = MCP230XX_GPIO(bus, address, gpio_count)

# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=1, pin_e=2, pins_db=[3,4,5,6], GPIO=mcp, pin_b=7)
lcd.begin(16, 2)
lcd.backlight(True)
lcd.clear()
lcd.message("  Adafruit 16x2\n  Standard LCD")
time.sleep(1)
lcd.clear()
lcd.message(" Hello ")
time.sleep(1)

num=0
while(True):
	lcd.setCursor(7, 0)
	lcd.message(str(num))
	num+=1
	if(num>9):
		num=0
	time.sleep(1)
