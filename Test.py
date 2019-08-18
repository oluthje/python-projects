# importing only those functions 
# which are needed 
from Tkinter import * 
#from tkinter.ttk import *
  
# creating tkinter window 
root = Tk() 
  
# Adding widgets to the root window 
Label(root, text = 'GeeksforGeeks', font =( 
  'Verdana', 15)).pack(side = TOP, pady = 10) 
  
# Creating a photoimage object to use image 
photo = PhotoImage(file = r"greencheckmark.gif")
Button(root, text = 'Click Me !', image = photo, height = 20, width = 20).pack(side = TOP)
  
mainloop() 