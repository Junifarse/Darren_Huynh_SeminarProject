import Tkinter as tk
from Tkinter import *


LARGE_FONT= ("Verdana", 12)
#Linked Frame

class InventoryMGMT(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

#Start Page        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Inventory Management", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
    
        button = tk.Button(self, text="Create Entry",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = tk.Button(self, text="Edit Entry",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

#Create Entry Page
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Create Entry", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        #User Entry
        

##
        Label(self,text="Serial Number").grid(row=0)
        Label(self,text="Tag Number").grid(row=1)
        Label(self,text="Shipdate").grid(row=2)
        Label(self,text="Location").grid(row=3)

        serial = Entry(self)
        tag = Entry(self)
        ship =Entry(self)
        location = Entry(self)
        
        serial.grid(row=0,column=1)
        tag.grid(row=1,column=1)
        ship.grid(row=2,column=1)
        location.grid(row=3,column=1)
        
##        button2 = tk.Button(self, text="Edit Entry",
##                            command=lambda: controller.show_frame(PageTwo))
##        button2.pack(side= BOTTOM)
##        
##        
##        button1 = tk.Button(self, text="Return To Menu",
##                            command=lambda: controller.show_frame(StartPage))
##        button1.pack(side=BOTTOM)

        
#Edit Entry Page

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Edit Entry", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Return To Menu",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(side=BOTTOM)

        button2 = tk.Button(self, text="Create Enty",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()
        


app = InventoryMGMT()
app.mainloop()
