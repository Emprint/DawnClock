# Sample code for both the RotaryEncoder class and the Switch class.
# The common pin for the encoder should be wired to ground.
# The sw_pin should be shorted to ground by the switch.

import gaugette.rotary_encoder
import gaugette.switch
import signal
import sys
import os
from Adafruit.LCD.Adafruit_CharLCD import Adafruit_CharLCD
from Adafruit.LCD.Adafruit_MCP230xx import MCP230XX_GPIO
import time

A_PIN  = 16
B_PIN  = 4 
SW_PIN = 15

encoder = gaugette.rotary_encoder.RotaryEncoder(A_PIN, B_PIN)
#encoder.start()
switch = gaugette.switch.Switch(SW_PIN)
last_state = None
lcd = None

soundVolume = 50
def VolumeUp():
	global soundVolume
	soundVolume = soundVolume + 1
	if soundVolume > 100:
		soundVolume = 100

	UpdateVolume()

	
def VolumeDown():
	global soundVolume
	soundVolume = soundVolume - 1
	if soundVolume < 0:
		soundVolume = 0

	UpdateVolume()
	

def UpdateVolume(amount = 0):
	global soundVolume, lcd
	if abs(amount) != 0:
		#Limit to 1 increments for more precision
		if amount > 1:
			amount = 1
		elif amount < 1:
			amount = -1
		#if amount == 2:
                #        amount = 1
                #elif amount == -2:
                #        amount = -1
		#else:
	#		amount = 0

		soundVolume = soundVolume + amount
		if soundVolume > 100:
			soundVolume = 100
		elif soundVolume < 0:
			soundVolume = 0
	print("Volume: " + str(soundVolume))
	os.system("amixer sset Master " +  str(soundVolume) + "% > /dev/null")
	lcd.setCursor(len("Volume "), 0)
        lcd.message(str(soundVolume).rjust(3))

def initLCD():
	global lcd, soundVolume
	bus = 1         # Note you need to change the bus number to 0 if running on a r$
	address = 0x20  # I2C address of the MCP230xx chip.
	gpio_count = 8  # Number of GPIOs exposed by the MCP230xx chip, should be 8 or $

	# Create MCP230xx GPIO adapter.
	mcp = MCP230XX_GPIO(bus, address, gpio_count)

	# Create LCD, passing in MCP GPIO adapter.
	lcd = Adafruit_CharLCD(pin_rs=1, pin_e=2, pins_db=[3,4,5,6], GPIO=mcp, pin_b=7)
	lcd.begin(16, 2)
	lcd.backlight(True)
	lcd.clear()
	lcd.message("Volume " + str(soundVolume).rjust(3) + "%")


def run_program():
	global sw_state, last_state, soundVolume
	initLCD()
	UpdateVolume()

	while True:
#    		delta = encoder.get_delta()
		delta = encoder.get_cycles()

    		if delta!=0:
#        		print ("rotate %d" % delta)
        		UpdateVolume(-delta)

    #if delta == -1:
#	VolumeUp()
 #   elif delta == 1:
#	VolumeDown()

    		sw_state = switch.get_state()
    		if sw_state != last_state:
        		print ("switch %d" % sw_state)
        		last_state = sw_state
			if sw_state == 1:
				soundVolume = 50
				UpdateVolume()
	time.sleep(0.001)	

def exit_gracefully(signum, frame):
    global encoder
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
		quit()

    except KeyboardInterrupt:
        print("Ok ok, quitting")
        quit()

    # restore the exit gracefully handler here    
    signal.signal(signal.SIGINT, exit_gracefully)

def quit():
	global encoder, lcd
#	encoder.stop()
	lcd.clear()
	lcd.backlight(False)
	sys.exit(1)

if __name__ == '__main__':
    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    run_program()
