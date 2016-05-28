# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import signal
import sys
pin1 = 12
pin2 = 16

def run_program():
        global pin1, pin2                   
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.setup(pin2, GPIO.OUT)

        while True:
                GPIO.output(pin1, True)
		time.sleep(1)
		GPIO.output(pin1, False)
		time.sleep(1)
		GPIO.output(pin2, True)
		time.sleep(1)
		GPIO.output(pin2, False)
		time.sleep(1)


def exit_gracefully(signum, frame):
        # restore the original signal handler as otherwise evil things will happen
        # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
        signal.signal(signal.SIGINT, original_sigint)

        
	global pin1, pin2
        GPIO.output(pin1, False)
        GPIO.output(pin2, False)
        sys.exit(1)

        # restore the exit gracefully handler here    
        signal.signal(signal.SIGINT, exit_gracefully)


def quit():
	global pin1, pin2
	GPIO.output(pin1, False)
	GPIO.output(pin2, False)
        sys.exit(1)

if __name__ == '__main__':
        # store the original SIGINT handler
        original_sigint = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, exit_gracefully)
        run_program()
