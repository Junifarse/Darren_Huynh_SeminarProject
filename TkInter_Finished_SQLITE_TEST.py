import Tkinter as tk
from Tkinter import *
import sqlite3 as lite
import sys
from tkMessageBox import*

#Filler Function

def say_hello():
    print "hello"
#Sqlite Cursor Connect
con = lite.connect('test.db',isolation_level=None)
with con:
    cur = con.cursor()

#Confirmation Popup
def clickCreate():
##    create=Toplevel()
##    label1=Label(create,text="Entry Created")
##    label1.pack()
##    okay_button = tk.Button(create,text='Okay',command=create.destroy)
##    okay_button.pack()
    showinfo(title='Entry Created',message="Entry Created")
#Empty Entry Popup
def emptyEntry():
##    empty=Toplevel()
##    label1= Label(empty,text="Error: Please Enter Serial/Tag")
##    label1.pack()
##    okay_button=tk.Button(empty,text='Okay',command=empty.destroy)
##    okay_button.pack()
    showwarning(title="Error",message="Enter Serial/Tag")
#Computer Exists Error Popup
def existEntry():
##    empty=Toplevel()
##    label1= Label(empty,text="Error: Computer Exists Already")
##    label1.pack()
##    okay_button=tk.Button(empty,text='Okay',command=empty.destroy)
##    okay_button.pack()
    showwarning(title="Error",message="Computer Exists Already")
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
        for F in (StartPage, CreatePage, EditPage,ViewPage):
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
        create_button = tk.Button(self, text="Create Entry",
                            command=lambda: controller.show_frame(CreatePage))
        create_button.pack()
        edit_button = tk.Button(self, text="Edit Entry",
                            command=lambda: controller.show_frame(EditPage))
        edit_button.pack()
        view_button = tk.Button(self, text ="View Entry",
                            command=lambda: controller.show_frame(ViewPage))
        view_button.pack()
        quit_button=tk.Button(self,text="Quit",
                              command=lambda:controller.destroy())
        quit_button.pack()

        

#Create Entry Page
class CreatePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Create Entry", font=LARGE_FONT)
        label.grid(row=0,pady=10,padx=10)
        Label(self,text="Serial Number").grid(row=2)
        Label(self,text="Tag Number").grid(row=3)
        Label(self,text="Shipdate").grid(row=4)
        Label(self,text="Location").grid(row=5)

        serial = Entry(self)
        tag = Entry(self)
        ship =Entry(self)
        location = Entry(self)
        serial.grid(row=2,column=1)
        tag.grid(row=3,column=1)
        ship.grid(row=4,column=1)
        location.grid(row=5,column=1)
        #Function to create Computer entry, and store it in database
        
        def create_entry():
            #Gets user input, clears upon button press
            serial_entry=serial.get()
            serial.delete(0,END)
            tag_entry=tag.get()
            tag.delete(0,END)
            ship_entry=ship.get()
            ship.delete(0,END)
            location_entry=location.get()
            location.delete(0,END)
            #Error Catch if Serial or Tag is blank, or if computer exists already no change
            if (serial_entry != '')and (tag_entry != ''):
                try:
                    cur.execute("Insert INTO Computers(Serial,Tag,ship,location) Values(?,?,?,?);",
                                (serial_entry,tag_entry,ship_entry,location_entry))
                    clickCreate()
                except:
                    existEntry()
                    
            else:
                emptyEntry()
                    
                    
           
            
        #Buttons
        enter_button= tk.Button(self, text ="Enter",command = create_entry)
        enter_button.grid(row=1,column=2)
        edit_button = tk.Button(self, text="Edit Entry",
                           command=lambda: controller.show_frame(EditPage))
        edit_button.grid(row=3,column=2)
        view_button= tk.Button(self, text="View Entry",
                               command=lambda:controller.show_frame(ViewPage))
        view_button.grid(row=4,column=2)
        return_button = tk.Button(self, text="Return To Menu",
                            command=lambda: controller.show_frame(StartPage))
        return_button.grid(row=5,column=2)

#Edit Entry Page

class EditPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Edit Entry", font=LARGE_FONT)
        label.grid(row=0,pady=10,padx=10)
        Label(self,text="Serial Number").grid(row=2)
        Label(self,text='OR').grid(row=3)
        Label(self,text="Tag Number").grid(row=4)
        

        serial = Entry(self)
        tag = Entry(self)
        ship =Entry(self)
        location = Entry(self)
        serial.grid(row=2,column=1)
        tag.grid(row=4,column=1)

        enter_button= tk.Button(self, text ="Enter",command = say_hello)
        enter_button.grid(row=1,column=2)
    
        create_button = tk.Button(self, text="Create Entry",
                            command=lambda: controller.show_frame(CreatePage))
        create_button.grid(row=3,column=2)

        view_button= tk.Button(self, text="View Entry",
                               command=lambda:controller.show_frame(ViewPage))
        view_button.grid(row=4,column=2)

        return_button = tk.Button(self, text="Return To Menu",
                            command=lambda: controller.show_frame(StartPage))
        return_button.grid(row=5,column=2)
        
class ViewPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="View Entry", font=LARGE_FONT)
        label.grid(row=0,pady=10,padx=10)
        Label(self,text="Serial Number").grid(row=2)
        Label(self,text='OR').grid(row=3)
        Label(self,text="Tag Number").grid(row=4)
        

        serial = Entry(self)
        tag = Entry(self)
        ship =Entry(self)
        location = Entry(self)
        serial.grid(row=2,column=1)
        tag.grid(row=4,column=1)
        

        enter_button= tk.Button(self, text ="Enter",command = say_hello)
        enter_button.grid(row=1,column=2)
        
        

        create_button = tk.Button(self, text="Create Entry",
                            command=lambda: controller.show_frame(CreatePage))
        create_button.grid(row=3,column=2)

        edit_button = tk.Button(self, text="Edit Entry",
                            command=lambda: controller.show_frame(EditPage))
        edit_button.grid(row=4,column=2)

        return_button = tk.Button(self, text="Return To Menu",
                            command=lambda: controller.show_frame(StartPage))
        return_button.grid(row=5,column=2)
    

app = InventoryMGMT()
app.mainloop()
