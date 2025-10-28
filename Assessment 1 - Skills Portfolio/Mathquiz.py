from tkinter import *
import tkinter
 
root = Tk()
Label(root, text="Check Buttons to select your level").pack(anchor = W)
C1 = Checkbutton(root, text = "Easy")
C2 = Checkbutton(root, text = "Medium")
C3 = Checkbutton(root, text = "Hard")
C1.pack(anchor = W )
C2.pack(anchor = W )
C3.pack(anchor = W )
root.mainloop()
