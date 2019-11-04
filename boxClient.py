import requests
import json
import string
import random

class boxClient:
	def __init__(self):
		API_KEY = '548451321avav'
		authorizationValue = 'Bearer ' + API_KEY;
		self.url = 'http://localhost:8000/api/compartments/'
		self.headers = {'content-type': 'application/json', 'Accept': 'application/json', 'Authorization': authorizationValue}
		
	def changePasscode(self, compartmentNumber, passcode, act):
		self.url = self.url + compartmentNumber
		self.act = act;
		myobj = {'act': act, 'passcode': passcode}
		x = requests.put(self.url, data = json.dumps(myobj), headers=self.headers)
		print(x)
