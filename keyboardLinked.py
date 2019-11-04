'''Popup Keyboard is a module to be used with Python's Tkinter library
It subclasses the Entry widget as KeyboardEntry to make a pop-up
keyboard appear when the widget gains focus. Still early in development.
'''

from tkinter import *
import time
from threading import Thread
import glob
from subscriptionMechanism import Subject, Observer
from typing import List

class Rows(Frame):
    def __init__(self, parent=None, **kwargs):
        Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky="nsew")
    def addRow(self, **kwargs):
        for attr in kwargs.keys():
            self.__dict__[attr] = kwargs[attr]

class _PopupKeyboard(Toplevel):
    '''A Toplevel instance that displays a keyboard that is attached to
    another widget. Only the Entry widget has a subclass in this version.
    '''
    
    def __init__(self, parent, attach, x, y, keycolor, linkVar, keysize=5):
        Toplevel.__init__(self, takefocus=0)
        
        self.overrideredirect(True)
        self.attributes('-alpha',0.85)

        self.parent = parent
        self.attach = attach
        self.keysize = keysize
        self.keycolor = keycolor
        self.x = x
        self.y = y
        self.config(cursor='none')
        self.linkVar = linkVar
        
#        self.rows = Rows(parent=self)
#        self.rows.addRow(row1=Frame(self.rows), row2= Frame(self.rows), row3=Frame(self.rows), row4=Frame(self.rows))

        
        # Specify number of layers in keyboard frame
        self.layer1 = Rows(parent=self)
        self.layer2 = Rows(parent=self) #equivalent to self.layer2 = Frame(self) since Rows inherits Frame
        
        # Layer One Keyboard Frame

        self.layer1.addRow(row1=Frame(self.layer1), row2= Frame(self.layer1), row3=Frame(self.layer1), row4=Frame(self.layer1))
        self.layer1.row1.grid(row=1)
        self.layer1.row2.grid(row=2)
        self.layer1.row3.grid(row=3)
        self.layer1.row4.grid(row=4)        

        
        # Layer Two Keyboard Frame
        self.layer2.addRow(row1=Frame(self.layer2), row2= Frame(self.layer2), row3=Frame(self.layer2), row4=Frame(self.layer2))
        self.layer2.row1.grid(row=1)
        self.layer2.row2.grid(row=2)
        self.layer2.row3.grid(row=3)
        self.layer2.row4.grid(row=4)        
        
        self._init_keys()
        self.layer1.tkraise()
        #self.pack() ##?? needed??
        
        # destroy _PopupKeyboard on keyboard interrupt
        self.bind('<Key>', lambda e: self._destroy_popup())

        # resize to fit keys
        self.update_idletasks()
        self.geometry('{}x{}+{}+{}'.format(self.winfo_width(),
                                           self.winfo_height(),
                                           self.x,self.y))
                              
                              
    
                                           
    def _create_buttons(self, layer):
        for row in self.layer_layout.keys():
            for i, k in enumerate(self.layer_layout[row]):
                Button(getattr(getattr(self, layer), row),
                       text=k,
                       width=self.keysize,
                       bg=self.keycolor,
                       command=lambda k=k: self._attach_key_press(k)).grid(row=0,column=i)            

        
    def _init_keys(self):
        self.keyboardLayers = {
            'layer1' : {
                'row1' : ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                'row2' : ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p','<-'],
                'row3' : ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',';'],
                'row4' : ['shift','z', 'x', 'c', 'v', 'b', 'n', 'm', 'shift']
            },
            'layer2' : {
                'row1' : ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                'row2' : ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P','<-'],
                'row3' : ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',';'],
                'row4' : ['SHIFT','Z', 'X', 'C', 'V', 'B', 'N', 'M','SHIFT']            
            }
        }
        
        for layer, layer_layout in self.keyboardLayers.items():
            self.layer_layout = layer_layout
            self._create_buttons(layer)
        
    def _destroy_popup(self):
        self.destroy()

    def _attach_key_press(self, k):
        if k == 'shift':
            self.layer2.tkraise()
        elif k == 'SHIFT':
            self.layer1.tkraise()
        elif k == '<-':
            self.remaining = self.attach.get()[:-1]
            self.attach.delete(0, END)
            self.attach.insert(0, self.remaining)
            s = self.attach.get()
            self.linkVar.set(s)
        else:
            self.attach.insert(END, k)
            s = self.attach.get()
            self.linkVar.set(s)

class PassCodes(Frame, Subject):
    
    _state: bool = False
    _observers: List[Observer] = []
    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)
    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)
    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)
    
    
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent)
        self.parent = parent
        
        self.pc1 = StringVar()
        entry1 = Label(self, textvariable=self.pc1, bg="white", relief='sunken', *args, **kwargs)
        entry1.pack(side='left')
        self.pc2 = StringVar()
        entry2 = Label(self, textvariable=self.pc2, bg="white", relief='sunken', *args, **kwargs)
        entry2.pack(side='left')
        self.pc3 = StringVar()
        entry3 = Label(self, textvariable=self.pc3, bg="white", relief='sunken', *args, **kwargs)
        entry3.pack(side='left')
        self.pc4 = StringVar()
        entry4 = Label(self, textvariable=self.pc4, bg="white", relief='sunken', *args, **kwargs)
        entry4.pack(side='left')
        self.pc5 = StringVar()
        entry5 = Label(self, textvariable=self.pc5, bg="white", relief='sunken', *args, **kwargs)
        entry5.pack(side='left')
        self.pc6 = StringVar()
        entry6 = Label(self, textvariable=self.pc6, bg="white", relief='sunken', *args, **kwargs)
        entry6.pack(side='left')
        
    def updateCodeSquare(self, n, m, x, entryText, var2):
        entryTextS = entryText.get()
        self.var2 = var2
        if len(entryTextS) == 0:
            self._state = False
            self.pc1.set('')
            self.pc2.set('')
            self.pc3.set('')
            self.pc4.set('')
            self.pc5.set('')
            self.pc6.set('')
        elif len(entryTextS) == 1:
            self._state = False
            self.pc1.set(entryTextS[0])
            self.pc2.set('')
            self.pc3.set('')
            self.pc4.set('')
            self.pc5.set('')
            self.pc6.set('')
        elif len(entryTextS) == 2:
            self._state = False
            self.pc1.set(entryTextS[0])
            self.pc2.set(entryTextS[1])
            self.pc3.set('')
            self.pc4.set('')
            self.pc5.set('')
            self.pc6.set('')
        elif len(entryTextS) == 3:
            self._state = False
            self.pc1.set(entryTextS[0])
            self.pc2.set(entryTextS[1])
            self.pc3.set(entryTextS[2])
            self.pc4.set('')
            self.pc5.set('')
            self.pc6.set('')
        elif len(entryTextS) == 4:
            self._state = False
            self.pc1.set(entryTextS[0])
            self.pc2.set(entryTextS[1])
            self.pc3.set(entryTextS[2])
            self.pc4.set(entryTextS[3])
            self.pc5.set('')
            self.pc6.set('')
        elif len(entryTextS) == 5:
            self._state = False
            self.pc1.set(entryTextS[0])
            self.pc2.set(entryTextS[1])
            self.pc3.set(entryTextS[2])
            self.pc4.set(entryTextS[3])
            self.pc5.set(entryTextS[4])
            self.pc6.set('')
        elif len(entryTextS) == 6:
            self._state = True
            self.pc1.set(entryTextS[0])
            self.pc2.set(entryTextS[1])
            self.pc3.set(entryTextS[2])
            self.pc4.set(entryTextS[3])
            self.pc5.set(entryTextS[4])
            self.pc6.set(entryTextS[5])
            #Thread(target=lambda var2=var2: self.clear_code(var2)).start()
            self.toCheckPasscode = self.pc1.get()+self.pc2.get()+self.pc3.get()+self.pc4.get()+self.pc5.get()+self.pc6.get()
            self.notify()
            entryText.set('')
            
            
            
    def clear_code(self, var2):
        print('no')
        time.sleep(1)
        self.toCheckPasscode = self.pc1.get()+self.pc2.get()+self.pc3.get()+self.pc4.get()+self.pc5.get()+self.pc6.get()
        self.pc1.set('')
        self.pc2.set('')
        self.pc3.set('')
        self.pc4.set('')
        self.pc5.set('')
        self.pc6.set('')
        var2.entry.delete(0, END)

        
        
        
        passcodes = glob.glob('somePassCodes/*.txt')
        #!!! check what happened if the users type very very fast
        for passcode in passcodes:
            readingFile = open(passcode, 'r')
            if toCheckPasscode == readingFile.readline():
                print(passcode + ' matched!')
            readingFile.close()


#            entryText.set('abc')
#            print(entryText.get())
#            print('done')

class ClearAllObserver(Observer):
    def clearCode(self, subject: Subject) -> None:
        print('no')
        time.sleep(1)
        subject.pc1.set('')
        subject.pc2.set('')
        subject.pc3.set('')
        subject.pc4.set('')
        subject.pc5.set('')
        subject.pc6.set('')
        subject.var2.entry.delete(0, END)
        
    def update(self, subject: Subject) -> None:
        if subject._state == True:
            Thread(target=lambda subject=subject: self.clearCode(subject)).start()
            #Thread(target=lambda subject=subject: self.clearCode(subject)).start()
        

class SubmitObserver(Observer):
    def submitCode(self, subject: Subject) -> None:
        print('no')
        time.sleep(1)
        toCheckPasscode = subject.pc1.get()+subject.pc2.get()+subject.pc3.get()+subject.pc4.get()+subject.pc5.get()+subject.pc6.get()            
        subject.pc1.set('')
        subject.pc2.set('')
        subject.pc3.set('')
        subject.pc4.set('')
        subject.pc5.set('')
        subject.pc6.set('')
        subject.var2.entry.delete(0, END)
        
    def update(self, subject: Subject) -> None:
        if subject._state == True:
            Thread(target=lambda subject=subject: self.submitCode(subject)).start()




class KeyboardEntry(Frame):
    '''An extension/subclass of the Tkinter Entry widget, capable
    of accepting all existing args, plus a keysize and keycolor option.
    Will pop up an instance of _PopupKeyboard when focus moves into
    the widget

    Usage:
    KeyboardEntry(parent, keysize=6, keycolor='white').pack()
    '''
    
    def __init__(self, parent, linkVar, keysize=5, keycolor='gray', *args, **kwargs):
        Frame.__init__(self, parent)
        self.parent = parent
        
        self.entry = Entry(self, *args, **kwargs)
        self.entry.pack()
#        self.entry.place(
        self.linkVar = linkVar
        self.keysize = keysize
        self.keycolor = keycolor
        
        self.state = 'idle'
        
        self.entry.bind('<FocusIn>', lambda e: self._check_state('focusin'))
        self.entry.bind('<FocusOut>', lambda e: self._check_state('focusout'))
        self.entry.bind('<Key>', lambda e: self._check_state('keypress'))

    def _check_state(self, event):
        '''finite state machine'''
        if self.state == 'idle':
            if event == 'focusin':
                self._call_popup()
                self.state = 'virtualkeyboard'
        elif self.state == 'virtualkeyboard':
            if event == 'focusin':
                self._destroy_popup()
                self.state = 'typing'
            elif event == 'keypress':
                self._destroy_popup()
                self.state = 'typing'
        elif self.state == 'typing':
            if event == 'focusout':
                self.state = 'idle'
        
    def _call_popup(self):
        self.kb = _PopupKeyboard(attach=self.entry,
                                 parent=self.parent,
                                 x=2,
                                 y=400,
                                 keysize=self.keysize,
                                 keycolor=self.keycolor,
                                 linkVar = self.linkVar)

    def _destroy_popup(self):
        self.kb._destroy_popup()

def checkLength(n, m, x, var):
    length = len(var.get())
    print(var.get())
#    if length == 6:
#        var2.entry.delete(0, END)

#    if (length == 6):
#        var.set('')
        
def test():  
    root = Tk()
    top_frame = Frame(root, width=640, height=480)
    top_frame.pack()
    linkVar = StringVar()
    k0 = PassCodes(top_frame, width=2, font=('courier',10, 'bold'))
    k0.pack()
    
    
#    linkVar.set('abef')
    k3 = KeyboardEntry(root, keysize=6, keycolor='white', linkVar=linkVar)
    k3.pack()
    k3.entry.place(x=700, y=700)   
    k3.entry.focus()
    linkVar.trace('w', lambda n,m,x,entryText=linkVar, var2=k3:k0.updateCodeSquare(n,m,x,entryText, var2))
    linkVar.trace('w', lambda n,m,x,var=linkVar:checkLength(n,m,x,var))
    root.mainloop()
