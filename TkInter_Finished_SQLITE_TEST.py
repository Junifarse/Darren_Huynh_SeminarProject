import Tkinter as tk
from Tkinter import *
import sqlite3 as lite
from tkMessageBox import*
import datetime
import time
import sys

#Filler Function

def say_hello():
    print "hello"

#Sqlite Cursor Connect
con = lite.connect('test.db',isolation_level=None)
with con:
    cur = con.cursor()

#Confirmation/Message Boxes Popup
def clickCreate():
    showinfo(title='Entry Created',message="Entry Created")
def clickEdit():
    showinfo(title='Entry Edited',message="Entry Edited")
    
#Empty Entry Popup
def emptyEntry():

    showwarning(title="Error",message="Enter Serial/Tag")
#Computer Exists Error Popup
def existEntry():

    showwarning(title="Error",message="Computer Exists Already")

def notexistEntry():
    showwarning(title="Error",message="Computer Does Not Exist")

def displayInfo():
    showinfo(title='Information',message=output)

    
#write create event to changelog
def writecreate(serial,tag):
    today = str(datetime.date.today())
    changelog=open('testchange.txt','a')
    changelog.write("CREATE COMPUTER SERIAL: " + serial+" TAG: " +tag+" DATE: "+today+"\n")
    changelog.close()
def writeEdit(serial,tag,ship,location):
    today = str(datetime.date.today())
    changelog=open('testchange.txt','a')
    changelog.write("EDIT COMPUTER SERIAL: " + serial+" TAG: " +tag+
                    " SHIP: "+str(ship)+" LOCATION: "+str(location)+" DATE: "+today+"\n")
    changelog.close()



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
        for F in (StartPage, CreatePage, EditPage,EditEntryPage,ViewPage,SummaryPage):
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
        summary_button =tk.Button(self,text="View Summary",
                                  command=lambda:controller.show_frame(SummaryPage))
        summary_button.pack()
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
                    writecreate(serial_entry,tag_entry)
                    
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


        def check_entry():
            #Gets user input, clears upon button press
            serial_entry=serial.get()
            serial.delete(0,END)
            tag_entry=tag.get()
            tag.delete(0,END)
            
            
            #Error Catch if Serial or Tag is blank, or if computer exists already no change
            if (serial_entry != '')or (tag_entry != ''):
                try:
                    cur.execute("SELECT * from Computers where Serial=? or Tag=?",(serial_entry,tag_entry))
                    rows = cur.fetchall()
                    checkerino=rows[0]
                    
                    global masterserial
                    if serial_entry!='':
                        masterserial=serial_entry
                    else:
                        masterserial = checkerino[0]                                        
                    controller.show_frame(EditEntryPage)
                except:
                    notexistEntry()
                    
            else:
                emptyEntry()
        enter_button= tk.Button(self, text ="Enter",command = check_entry)
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

class EditEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter Edits", font=LARGE_FONT)
        label.grid(row=0,pady=10,padx=10)
        
        Label(self,text="Tag Number").grid(row=3)
        Label(self,text="Shipdate").grid(row=4)
        Label(self,text="Location").grid(row=5)
        tag = Entry(self)
        ship =Entry(self)
        location = Entry(self)
        tag.grid(row=3,column=1)
        ship.grid(row=4,column=1)
        location.grid(row=5,column=1)

        def check_entry():
            #Gets user input, clears upon button press
            tag_entry=tag.get()
            tag.delete(0,END)
            ship_entry=ship.get()
            ship.delete(0,END)
            location_entry=location.get()
            location.delete(0,END)
            cur.execute("SELECT * FROM Computers where Serial = ?",[masterserial])
            rows= cur.fetchall()
            checkerino=rows[0]
            if tag_entry=='':
                tag_entry=checkerino[1]
            if ship_entry=='':
                ship_entry=checkerino[2]
            if location_entry=='':
                location_entry=checkerino[3]
            cur.execute("UPDATE Computers SET tag =?,ship=?,location=? WHERE serial=?",
                        (tag_entry,ship_entry,location_entry,masterserial))
            clickEdit()
            writeEdit(masterserial,tag_entry,ship_entry,location_entry)
            controller.show_frame(EditPage)


        enter_button= tk.Button(self, text ="Enter",command = check_entry)
        enter_button.grid(row=1,column=2)



        
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
        serial.grid(row=2,column=1)
        tag.grid(row=4,column=1)
        def view_entry():
            #Gets user input, clears upon button press
            serial_entry=serial.get()
            serial.delete(0,END)
            tag_entry=tag.get()
            tag.delete(0,END)
            
            #Error Catch if Serial or Tag is blank, or if computer exists already no change
            if (serial_entry != '')or (tag_entry != ''):
                try:
                    cur.execute("SELECT * from Computers where Serial=? or Tag=?",(serial_entry,tag_entry))
                    rows = cur.fetchall()
                    if len(rows)== 0:
                        notexistEntry()
                    else:
                        global output
                        convert=rows[0]
                        
                        ttserial= "Serial: "+convert[0]
                        tttag = "\nTag: " + convert[1]
                        ttship="\nShip: " + str(convert[2])
                        ttlocation="\nLocation: " +str(convert[3])
                        
                        output= ttserial+tttag+ttship+ttlocation
                    
                        
                        displayInfo()                 
                except:
                    notexistEntry()   
            else:
                emptyEntry()
        enter_button= tk.Button(self, text ="Enter",command = view_entry)
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
    

class SummaryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Summary", font=LARGE_FONT)
        label.grid(row=0,pady=10,padx=10)

        cur.execute("SELECT * FROM Computers ORDER BY tag,location")
        rows = cur.fetchall()
        alloutput=""
        for row in rows:
            
            ttserial= "Serial: "+row[0]
            tttag = " Tag: " + row[1]
            ttship=" Ship: " + str(row[2])
            ttlocation=" Location: " +str(row[3])
            
            output= ttserial+tttag+ttship+ttlocation+"\n"
            alloutput+=output
        
        information= tk.Label(self,text=alloutput)
        information.grid(row=1,column=0)

        return_button = tk.Button(self, text="Return To Menu",
                            command=lambda: controller.show_frame(StartPage))
        return_button.grid(row=5,column=0)
        

app = InventoryMGMT()
app.mainloop()
