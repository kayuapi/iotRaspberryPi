from Compartments import *
import time
from subscriptionMechanism import Observer, Subject
from threading import Thread
from boxClient import boxClient

class Locker(Observer):
	def __init__(self):
		_location=''
		_unit = ''
		self.name = _location+'-'+_unit
		self.compartments = Compartments(compartmentNumber=3)
		self.apiKey = ''
		self.openCompartment = None
		for compartment in self.compartments:
			boxCli = boxClient()
			boxCli.changePasscode(str(compartment.id), compartment.passcode, 'poweringUpLocker')		
	
	def checkMatchedCompartments(self, passcode):
		for compartment in self.compartments:
			if passcode == compartment.passcode:
				self.openCompartment = compartment.id
				compartment.open()
				self.submitNewPasscode(compartment)
				print('Compartment ' + str(self.openCompartment) + ' is matched!')
			
		
	def submitNewPasscode(self, compartment):
		passcode = compartment.newPasscode()
		if compartment.emptied == 0:
			compartment.emptied = 1
			act = 'borrow'
		elif compartment.emptied == 1:
			compartment.emptied = 0
			act = 'return'
		print(compartment.id)
		print(passcode)
		boxCli = boxClient()
		boxCli.changePasscode(str(compartment.id), passcode, act)			
		
		#time.ctime(time.time())
		
	def update(self, subject: Subject) -> None:
		if subject._state == True:
			Thread(target=lambda subject=subject: self.checkMatchedCompartments(subject.toCheckPasscode)).start()
