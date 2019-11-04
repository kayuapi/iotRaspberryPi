from keyboardLinked import KeyboardEntry
from keyboardLinked import PassCodes, ClearAllObserver
import keyboardLinked as kb
import tkinter as tk
import os
import boxClient
from Locker import Locker

class App:
    
	def __init__(self, window, window_title):
		self.window = window
		self.window.title(window_title)
		self.window.config(cursor='none')
		top_frame = tk.Frame(self.window, width=480, height=800)
		top_frame.pack(side='top')
		top_frame.place(x=15,y=200)     
		linkVar = tk.StringVar()
		k0 = PassCodes(top_frame, width=2, font=('courier',45, 'bold'))
		k0.pack()



		bottom_frame = tk.Frame(self.window, width=480, height=800)
		bottom_frame.pack(side='bottom')
		bottom_frame.place(x=15,y=450)     

	#    linkVar.set('abef')
		k3 = KeyboardEntry(bottom_frame, keysize=2, keycolor='white', linkVar=linkVar)
		
		k3.pack()
		
#		k3.entry.place(x=50, y=150)   
		k3.entry.focus()

		linkVar.trace('w', lambda n,m,x,var=linkVar:kb.checkLength(n,m,x,var))    		
		linkVar.trace('w', lambda n,m,x,entryText=linkVar, var2=k3:k0.updateCodeSquare(n,m,x,entryText,var2))

		k0.attach(ClearAllObserver())
		k0.attach(Locker())
		#boxClient = boxClient()
		#boxClient.changePasscode(compartmentNumber, passcode, act)	
		#k0.toCheckPasscode
		
		
		
		

		self.window.attributes("-fullscreen", True)
		#self.window.wm_attributes("-topmost", True)
		self.window.bind("<Escape>", self.on_escape)
#		self.window.after(30000, self.window.destroy)
		self.window.mainloop()




	def on_escape(self, event=None):
		print('escaped')
		self.window.destroy()
		

App(tk.Tk(), "Cong He Meng")
