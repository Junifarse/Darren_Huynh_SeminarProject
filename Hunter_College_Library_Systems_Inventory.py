import Tkinter as tk
from Tkinter import *
import sqlite3 as lite
from tkMessageBox import*
import datetime,time,sys,ttk,os.path

#Checks for Computers Database
if os.path.isfile('Computers.db'):
    con = lite.connect('Computers.db',isolation_level=None)
    with con:
        cur = con.cursor()
else:
    #Creates it if its missing
    con = lite.connect('Computers.db')

    with con:
            
        cur = con.cursor()    
        cur.execute("CREATE TABLE Computers(Serial TEXT PRIMARY KEY NOT NULL,Tag TEXT  NOT NULL, Ship INT, Location INT);")

   
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
#Computer does not exist Error Popup
def notexistEntry():
    showwarning(title="Error",message="Computer Does Not Exist")
#Display Specific Computer Information from View Entry
def displayInfo():
    showinfo(title='Information',message=output)
#Generate Summary Page
def summary():
    class Summary(Tk):
        def __init__(self, parent):
            Tk.__init__(self, parent)
            self.title("Summary Page")
            cur.execute("SELECT * FROM Computers ORDER BY tag,location")
            rows = cur.fetchall()
            serialgrid=''
            taggrid=''
            shipgrid=''
            locationgrid=''
            for row in rows:
                serialgrid+=row[0]+'\n'
                taggrid+=row[1]+'\n'
                shipgrid+=str(row[2])+'\n'
                locationgrid+=str(row[3])+'\n'
            seriallabel=tk.Label(self,text='Serial',font=LARGE_FONT)
            seriallabel.grid(row=0,column=0)
            serialinformation = tk.Label(self,text=serialgrid)
            serialinformation.grid(row=1,column=0)
            taginformation = tk.Label(self,text=taggrid)
            taginformation.grid(row=1,column=1)
            taglabel=tk.Label(self,text='CUNYTAG',font=LARGE_FONT)
            taglabel.grid(row=0,column=1)
            shipinformation = tk.Label(self,text=shipgrid)
            shipinformation.grid(row=1,column=2)
            shiplabel=tk.Label(self,text='Shipdate',font=LARGE_FONT)
            shiplabel.grid(row=0,column=2)
            locationinformation = tk.Label(self,text=locationgrid)
            locationinformation.grid(row=1,column=3)
            locationlabel=tk.Label(self,text='Location',font=LARGE_FONT)
            locationlabel.grid(row=0,column=3)
    window=Summary(None)
    window.mainloop()
    
   
#write create event to changelog
def writecreate(serial,tag):
    today = str(datetime.date.today())
    currenttime= str(datetime.datetime.now().time())
    changelog=open('changelog.txt','a')
    changelog.write("CREATE COMPUTER SERIAL: " + serial+" TAG: " +tag+" DATE: "+today+
                    " TIME: "+currenttime+"\n")
    changelog.close()
#Write edit event to changelog
def writeEdit(serial,tag,ship,location):
    today = str(datetime.date.today())
    currenttime= str(datetime.datetime.now().time())
    changelog=open('changelog.txt','a')
    changelog.write("EDIT COMPUTER SERIAL: " + serial+" TAG: " +tag+
                    " SHIP: "+str(ship)+" LOCATION: "+str(location)+" DATE: "+today+
                    " TIME: "+currenttime+"\n")
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
        for F in (StartPage, CreatePage, EditPage,EditEntryPage,ViewPage):
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
                                  command=summary)
        summary_button.pack()
        quit_button=tk.Button(self,text="Quit",
                              command=lambda:controller.destroy())
        quit_button.pack()

        

#Create Entry Page
class CreatePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        stepOne = tk.LabelFrame(self, text=" Create Entry: ",font=LARGE_FONT)
        stepOne.grid(row=0, columnspan=5, rowspan=5,sticky='W', \
                 padx=10, pady=10, ipadx=10, ipady=10)
        Label(stepOne,text="Serial Number").grid(row=1)
        Label(stepOne,text="Tag Number").grid(row=2)
        Label(stepOne,text="Shipdate").grid(row=3)
        Label(stepOne,text="Location").grid(row=4)
        serial = Entry(stepOne)
        tag = Entry(stepOne)
        #Months Entry
        shipmonth =ttk.Combobox(stepOne,width=15)
        shipmonth['values']=('Jan','Feb','Mar','Apr','May','Jun','Jul',
                            'Aug','Sep','Oct','Nov','Dec')
        shipday=ttk.Combobox(stepOne,width=5)
        #Day Entry
        shipday['values']=('1','2','3','4','5','6','7','8','9',
                           '10','11','12','13','14','15','16'
                           ,'17','18','19','20','21','22','23','24','25',
                           '26','27','28','29','30','31')
        #Year Entry
        shipyear=ttk.Combobox(stepOne,width=5)
        shipyear['values']=('2016','2015','2014','2013','2012','2011',
                            '2010','2009','2008','2007','2006','2005','2004',
                            '2003','2002','2001','2000')
        #Location Entry "Floors"
        location = ttk.Combobox(stepOne,width=5)
        location['values']= ('B1','B2','1','2','3','4','5')
        serial.grid(row=1,column=1)
        tag.grid(row=2,column=1)
        shipmonth.grid(row=3,column=1)
        shipday.grid(row=3,column=2)
        shipyear.grid(row=3,column=3)
        location.grid(row=4,column=1)
        #Function to create Computer entry, and store it in database
        
        def create_entry():
            #Gets user input, clears upon button press
            serial_entry=serial.get()
            serial.delete(0,END)
            tag_entry=tag.get()
            tag.delete(0,END)
            ship_entry=shipmonth.get()+'-'+shipday.get()+'-'+shipyear.get()
            shipmonth.delete(0,END)
            shipday.delete(0,END)
            shipyear.delete(0,END)
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
        stepTwo = tk.LabelFrame(self, text= " Menu ",font=LARGE_FONT)
        stepTwo.grid(row=0, column=8,sticky='W', \
                 padx=5, pady=5, ipadx=5, ipady=5)
        enter_button= tk.Button(stepOne, text ="Enter",command = create_entry)
        enter_button.grid(row=4,column=5)
        edit_button = tk.Button(stepTwo, text="Edit Entry",
                           command=lambda: controller.show_frame(EditPage))
        edit_button.grid(row=3,column=2)
        view_button= tk.Button(stepTwo, text="View Entry",
                               command=lambda:controller.show_frame(ViewPage))
        view_button.grid(row=4,column=2)
        return_button = tk.Button(stepTwo, text="Return To Menu",
                            command=lambda: controller.show_frame(StartPage))
        return_button.grid(row=5,column=2)

#Edit Entry Page

class EditPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        stepOne = tk.LabelFrame(self, text=" Edit Entry: ",font=LARGE_FONT)
        stepOne.grid(row=0, columnspan=5, rowspan=5,sticky='W', \
                 padx=10, pady=10, ipadx=10, ipady=10)
        Label(stepOne,text="Serial Number").grid(row=2)
        Label(stepOne,text='OR').grid(row=3)
        Label(stepOne,text="Tag Number").grid(row=4)
        serial = Entry(stepOne)
        tag = Entry(stepOne)
        ship =Entry(stepOne)
        location = Entry(stepOne)
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

        stepTwo = tk.LabelFrame(self, text= " Menu ",font=LARGE_FONT)
        stepTwo.grid(row=0, column=9,sticky='W', \
                 padx=5, pady=5, ipadx=5, ipady=5)
        #Buttons
        enter_button= tk.Button(stepOne, text ="Enter",command = check_entry)
        enter_button.grid(row=4,column=5)
    
        create_button = tk.Button(stepTwo, text="Create Entry",
                            command=lambda: controller.show_frame(CreatePage))
        create_button.grid(row=3,column=2)

        view_button= tk.Button(stepTwo, text="View Entry",
                               command=lambda:controller.show_frame(ViewPage))
        view_button.grid(row=4,column=2)

        return_button = tk.Button(stepTwo, text="Return To Menu",
                            command=lambda: controller.show_frame(StartPage))
        return_button.grid(row=5,column=2)

class EditEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        stepOne = tk.LabelFrame(self, text=" Edit Entry: *Items left Blank will be Unchanged",font=LARGE_FONT)
        stepOne.grid(row=0, columnspan=5, rowspan=5,sticky='W', \
                 padx=10, pady=10, ipadx=10, ipady=10)
        
        Label(stepOne,text="Tag Number").grid(row=3)
        Label(stepOne,text="Shipdate").grid(row=4)
        Label(stepOne,text="Location").grid(row=5)
        tag = Entry(stepOne)
        ship =Entry(stepOne)
        location = Entry(stepOne)
        tag.grid(row=3,column=1)
        ship.grid(row=4,column=1)
        location.grid(row=5,column=1)

        def check_entry():
            #Gets user input, clears upon button press, Executes EDIT ENTRY
            tag_entry=tag.get()
            tag.delete(0,END)
            ship_entry=ship.get()
            ship.delete(0,END)
            location_entry=location.get()
            location.delete(0,END)
            cur.execute("SELECT * FROM Computers where Serial = ?",[masterserial])
            rows= cur.fetchall()
            checkerino=rows[0]
            #If Patron leaves entry blank = NO CHANGE
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


        enter_button= tk.Button(stepOne, text ="Enter",command = check_entry)
        enter_button.grid(row=5,column=2)



        
class ViewPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        stepOne = tk.LabelFrame(self, text=" View Entry: ",font=LARGE_FONT)
        stepOne.grid(row=0, columnspan=5, rowspan=5,sticky='W', \
                 padx=10, pady=10, ipadx=10, ipady=10)
        Label(stepOne,text="Serial Number").grid(row=2)
        Label(stepOne,text='OR').grid(row=3)
        Label(stepOne,text="Tag Number").grid(row=4)
        
        serial = Entry(stepOne)
        tag = Entry(stepOne)
        serial.grid(row=2,column=1)
        tag.grid(row=4,column=1)
        
        def view_entry():
            #Gets user input, clears upon button press
            serial_entry=serial.get()
            serial.delete(0,END)
            tag_entry=tag.get()
            tag.delete(0,END)
            
            #Error Catch if both Serial or Tag are blank
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
                    #Displays info for computer in a popup messagebox                  
                        displayInfo()                 
                except:
                    notexistEntry()   
            else:
                emptyEntry()
        #Buttons
        stepTwo = tk.LabelFrame(self, text= " Menu ",font=LARGE_FONT)
        stepTwo.grid(row=0, column=8,sticky='W', \
                 padx=5, pady=5, ipadx=5, ipady=5)
        enter_button= tk.Button(stepOne, text ="Enter",command = view_entry)
        enter_button.grid(row=4,column=2)
        create_button = tk.Button(stepTwo, text="Create Entry",
                            command=lambda: controller.show_frame(CreatePage))
        create_button.grid(row=3,column=2)
        edit_button = tk.Button(stepTwo, text="Edit Entry",
                            command=lambda: controller.show_frame(EditPage))
        edit_button.grid(row=4,column=2)
        return_button = tk.Button(stepTwo, text="Return To Menu",
                            command=lambda: controller.show_frame(StartPage))
        return_button.grid(row=5,column=2)
    


app = InventoryMGMT()
app.wm_title("Hunter College Library Systems Inventory Management")
app.mainloop()
