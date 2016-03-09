#!/usr/bin/python

import time
from Lib.Threads import LcdThread

alarm = None
class DawnClock:

	def __init__(self):
		self.stopping = False
		self.debug = True
		self.log("DawnClock starting")
		self.execute()
		
		
	def stop(self):
		self.log("DawnClock stopping")
		self.stopping = True
	
	
	def log(self, message):
		if self.debug:
			print(message)
		
			
	def execute(self):
		self.log("Loading LCD")
		lcd = LcdThread.LcdThread(self, self.stop)
		lcd.setDaemon(True)
		lcd.start()
      
		# Main loop where we just spin until we receive a shutdown request
		try:
			while(self.stopping is False):
				time.sleep(1)
		except (KeyboardInterrupt, SystemExit):
			self.log("Interrupted, shutting down")
			
		lcd.stop()


if __name__ == '__main__':
	alarm = DawnClock()