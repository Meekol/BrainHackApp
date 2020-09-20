import tkinter as tk
from tkinter import ttk
 
 
window = tk.Tk()
 
window.title("Brainhack Schedule App")
window.minsize(600,400)
 
def clickMe():
    label.configure(text= 'Hello ' + name.get())
 
def clickSchedule():
    print('do')
    
label = ttk.Label(window, text = "Enter Input")
label.grid(column = 0, row = 0)
 
 
name = tk.StringVar()
nameEntered = ttk.Entry(window, width = 15, textvariable = name)
nameEntered.grid(column = 0, row = 1)
 
 
button = ttk.Button(window, text = "Submit Info", command = clickMe)
button.grid(column= 0, row = 2)

button = ttk.Button(window, text = "Create Schedule", command = clickSchedule)
button.grid(column= 0, row = 3)
 
 
window.mainloop()
