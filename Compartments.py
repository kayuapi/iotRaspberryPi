import string
import random
import RPi.GPIO as GPIO
import time
from itertools import count



class Compartments(list):
	def __init__(self, compartmentNumber, *args, **kwargs):
		list.__init__(self, *args, **kwargs)
		for i in range(compartmentNumber):
			self.append(Compartment())

class Compartment:
	_ids = count(1)
	Relay_Ch1 = 26
	Relay_Ch2 = 20
	Relay_Ch3 = 21

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(Relay_Ch1,GPIO.OUT)
	GPIO.setup(Relay_Ch2,GPIO.OUT)
	GPIO.setup(Relay_Ch3,GPIO.OUT)
	GPIO.output(Relay_Ch1,GPIO.HIGH)
	GPIO.output(Relay_Ch2,GPIO.HIGH)
	GPIO.output(Relay_Ch3,GPIO.HIGH)
	
	print("Setup The Relay Module is [success]")
	
	def __init__(self):
		self.closed = True
		self.passcode = self._generatePasscode()
		print(self.passcode)
		self.emptied = 0
		self.id = next(self._ids)
		
	def newPasscode(self):
		self.passcode = self._generatePasscode()
		return self.passcode
		
	def getBorrowCode():
		pass
	def getReturnCode():
		pass
	def getAPI():
		pass
	def submitCodeToServer():
		pass
	
	def _generatePasscode(self, size=6, chars=string.ascii_letters + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))
	
	def open(self):
		if self.id == 1:
			GPIO.output(self.Relay_Ch1,GPIO.LOW)
			time.sleep(0.5)
			GPIO.output(self.Relay_Ch1,GPIO.HIGH)
		elif self.id == 2:
			GPIO.output(self.Relay_Ch2,GPIO.LOW)
			time.sleep(0.5)
			GPIO.output(self.Relay_Ch2,GPIO.HIGH)
		elif self.id == 3:
			GPIO.output(self.Relay_Ch3,GPIO.LOW)
			time.sleep(0.5)
			GPIO.output(self.Relay_Ch3,GPIO.HIGH)
		else:
			pass
