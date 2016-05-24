##Author: Darren Huynh for Hunter College CSCI 233 Seminar Project
##Description: Inventory Management Program
##Credits: SeaofBTC for Linked Frames Code


#import modules
#importing modules
import Tkinter as tk
from Tkinter import *
import sqlite3 as lite
from tkMessageBox import*
import datetime,time,sys,ttk,os.path
##list of months/days/years/locations
#Change default value by modifying first element in each list
months_list=[' - ','Jan','Feb','Mar','Apr','May','Jun','Jul',
                            'Aug','Sep','Oct','Nov','Dec']
days_list = [' - ','1','2','3','4','5','6','7','8','9',
                           '10','11','12','13','14','15','16'
                           ,'17','18','19','20','21','22','23','24','25',
                           '26','27','28','29','30','31']
#edit/add years here
years_list =[' - ','2016','2015','2014','2013','2012','2011',
                            '2010','2009','2008','2007','2006','2005','2004',
                            '2003','2002','2001','2000']
#add locations here
locations_list=[' - ','B1','B2','1','2','3','4','5']

#Checks for Computers Database
if os.path.isfile('Computers.db'):
    con = lite.connect('Computers.db',isolation_level=None)
    with con:
        cur = con.cursor()
else:
    #Creates it if its missing; rename db here
    con = lite.connect('Computers.db')
    with con:         
        cur = con.cursor()
        #edit table parameters here, ex: Model TEXT,
        cur.execute("CREATE TABLE Computers(Serial TEXT NOT NULL,Tag TEXT  NOT NULL, Ship INT, Location INT, PRIMARY KEY(Serial,Tag));")

##Dialog Boxes
   
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
    
#Generate Dynamic Summary Page

def summary():
    class Summary(Tk):
        def __init__(self, parent):
            Tk.__init__(self, parent)
            self.title("Summary Page")
            frameOne = tk.LabelFrame(self)
            frameOne.grid(row=0, columnspan=5, rowspan=5,sticky='W', \
                 padx=10, pady=10, ipadx=10, ipady=10)
            #fetches information from all computers, ordered by tag and location
            cur.execute("SELECT * FROM Computers ORDER BY tag,location")
            rows = cur.fetchall()
            #enter additional information here as a blank string
            serialgrid=''
            taggrid=''
            shipgrid=''
            locationgrid=''
            #converts the "row information" from the fetch and puts it into a string
            #and is displayed
            for row in rows:
                serialgrid+=row[0]+'\n'
                taggrid+=row[1]+'\n'
                shipgrid+=str(row[2])+'\n'
                locationgrid+=str(row[3])+'\n'
            #formatting information/labels mix and match grids here
            seriallabel=tk.Label(frameOne,text='Serial',font=LARGE_FONT)
            seriallabel.grid(row=0,column=0)
            serialinformation = tk.Label(frameOne,text=serialgrid)
            serialinformation.grid(row=1,column=0)
            taginformation = tk.Label(frameOne,text=taggrid)
            taginformation.grid(row=1,column=1)
            taglabel=tk.Label(frameOne,text='CUNYTAG',font=LARGE_FONT)
            taglabel.grid(row=0,column=1)
            shipinformation = tk.Label(frameOne,text=shipgrid)
            shipinformation.grid(row=1,column=2)
            shiplabel=tk.Label(frameOne,text='Shipdate',font=LARGE_FONT)
            shiplabel.grid(row=0,column=2)
            locationinformation = tk.Label(frameOne,text=locationgrid)
            locationinformation.grid(row=1,column=3)
            locationlabel=tk.Label(frameOne,text='Location',font=LARGE_FONT)
            locationlabel.grid(row=0,column=3)
    window=Summary(None)
    window.mainloop()

def admin():
    class Admin(Tk):
        def __init__(self,parent):
            Tk.__init__(self,parent)
            self.title("Admin Login")
    #cautions the user that only authorized users should use this        
    question=askokcancel(title='Warning',message= 'Only Authorized Users Should Use This')
    if question is True:
        #create login prompt
        admin=Toplevel()
        admin.title('Admin Login')
        def checklogin():
            user=adminuserentry.get()
            password=adminpassentry.get()
            #delete entry function
            def delete_entry():
                serial_entry=serial.get()
                serial.delete(0,END)
                cur.execute("SELECT * from Computers where Serial=?",(serial_entry,))
                checkerino= cur.fetchall()
                #if computer exists, delete and then add to changelog
                if len(checkerino)!= 0:
                    cur.execute("DELETE FROM Computers WHERE Serial =?",(serial_entry,))
                    showinfo(title="Delete Complete", message="Entry Deleted")
                    writeDelete(serial_entry)
                    
                else:
                    #if computer does not exist
                    notexistEntry()
                    
            if (user  == 'Poseidon') and (password == 'Trident'):
                admin.destroy()
                adminfunction=Toplevel()
                adminfunction.title=('Admin Functions')
                Label(adminfunction,text="Serial Number").grid(row=0,column=0)
                serial = Entry(adminfunction)
                serial.grid(row=0,column=1)

                delete_button=tk.Button(adminfunction,text="Delete",
                                        command=delete_entry).grid(
                                            row=1,column=0)
                quit_button=tk.Button(adminfunction,text="Quit",
                              command=lambda :adminfunction.destroy()).grid(
                                  row=1,column=1)
            else:
                #incorrect login shows warning
                    showwarning(title='Invalid Username/Password',message=
                                'Invalid Username or Password')
        #labels and buttons            
        adminuserlabel=Label(admin,text='Admin User: ').grid(row=0,column=0)
        adminuserentry=Entry(admin)
        adminuserentry.grid(row=0,column=1)
        adminpasslabel=Label(admin,text='Password: ').grid(row=1,column=0)
        adminpassentry=Entry(admin,show="*")
        adminpassentry.grid(row=1,column=1)
        login_button=tk.Button(admin,text="Login",
                               command =lambda :checklogin()).grid(
                                   row=0,column=2)
        quit_button=tk.Button(admin,text="Quit",
                              command=lambda :admin.destroy()).grid(
                                  row=1,column=2)


##Changelog Writing   
   
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
    
def writeDelete(serial):
    today = str(datetime.date.today())
    currenttime= str(datetime.datetime.now().time())
    changelog=open('changelog.txt','a')
    changelog.write("DELETE COMPUTER SERIAL: " + serial +" DATE: "+today+
                    " TIME: "+currenttime+"\n")  



LARGE_FONT= ("Times New Roman", 12)
##Linked Frame Container/Object, Preloads all the Entry options upon initiation
class InventoryMGMT(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        #All the "Pages" are included here for preloading. Include future pages in this list
        for F in (StartPage, CreatePage, EditPage,EditEntryPage,ViewPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)
        
    #show frame function    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()       

##Start Page/Menu Contains all the buttons to access other pages     
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        #frame one for easier widget management
        frameOne = tk.LabelFrame(self,font=LARGE_FONT)
        frameOne.pack()
        label = tk.Label(frameOne, text="Hunter College Library Inventory Management", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #add buttons below, in consequent order because pack is used here
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
        admin_button = tk.Button(self,text = "Admin Login",
                                 command = admin)
        admin_button.pack()
        quit_button=tk.Button(self,text="Quit",
                              command=lambda:controller.destroy())
        quit_button=tk.Button(self,text="Quit",
                              command=lambda:controller.destroy())
        quit_button.pack()

        

##Create Entry Page; Data entry
class CreatePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #frame one for easier widget management
        frameOne = tk.LabelFrame(self, text=" Create Entry: ",font=LARGE_FONT)
        frameOne.grid(row=0, columnspan=5, rowspan=5,sticky='W', \
                 padx=10, pady=10, ipadx=10, ipady=10)
        Label(frameOne,text="Serial Number").grid(row=1)
        Label(frameOne,text="Tag Number").grid(row=2)
        Label(frameOne,text="Shipdate").grid(row=3)
        Label(frameOne,text="Location").grid(row=4)
        serial = Entry(frameOne)
        tag = Entry(frameOne)
        #Months Entry
        shipmonth =ttk.Combobox(frameOne,width=15)
        shipmonth['values']=months_list
        shipmonth.current(0)
        shipday=ttk.Combobox(frameOne,width=5)
        #Day Entry
        shipday['values']=days_list
        shipday.current(0)
        #Year Entry
        shipyear=ttk.Combobox(frameOne,width=5)
        shipyear['values']=years_list
        shipyear.current(0)
        #Location Entry "Floors"
        location = ttk.Combobox(frameOne,width=5)
        location['values']= locations_list
        location.current(0)
        
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
            shipmonth.current(0)
            shipday.current(0)
            shipyear.current(0)
            location_entry=location.get()
            location.current(0)
           
            
            #Error Catch if Serial or Tag is blank, or if computer exists already no change
            if (serial_entry != '')and (tag_entry != ''):
                try:
                    cur.execute("Insert INTO Computers(Serial,Tag,ship,location) Values(?,?,?,?);",
                                (serial_entry,tag_entry,ship_entry,location_entry))
                    clickCreate()
                    writecreate(serial_entry,tag_entry)
                    lambda:controller.show_frame(CreatePage)
                except:
                    existEntry()                    
            else:
                emptyEntry()
                
        #Menu Buttons in a second frame for easy button management in a second frame for easy button management
        frameTwo = tk.LabelFrame(self, text= " Menu ",font=LARGE_FONT)
        frameTwo.grid(row=0, column=8,sticky='W', \
                 padx=5, pady=5, ipadx=5, ipady=5)
        enter_button= tk.Button(frameOne, text ="Enter",command = create_entry)
        enter_button.grid(row=4,column=5)
        edit_button = tk.Button(frameTwo, text="Edit Entry",
                           command=lambda: controller.show_frame(EditPage))
        edit_button.grid(row=3,column=2)
        view_button= tk.Button(frameTwo, text="View Entry",
                               command=lambda:controller.show_frame(ViewPage))
        view_button.grid(row=4,column=2)
        return_button = tk.Button(frameTwo, text="Return To Menu",
                            command=lambda: controller.show_frame(StartPage))
        return_button.grid(row=5,column=2)

#Edit Entry Page

class EditPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #frame one for easier widget management
        frameOne = tk.LabelFrame(self, text=" Edit Entry: ",font=LARGE_FONT)
        frameOne.grid(row=0, columnspan=5, rowspan=5,sticky='W', \
                 padx=10, pady=10, ipadx=10, ipady=10)
        Label(frameOne,text="Serial Number").grid(row=2)
        Label(frameOne,text='AND').grid(row=3)
        Label(frameOne,text="Tag Number").grid(row=4)
        serial = Entry(frameOne)
        tag = Entry(frameOne)
        ship =Entry(frameOne)
        location = Entry(frameOne)
        serial.grid(row=2,column=1)
        tag.grid(row=4,column=1)
        
        def check_entry():
            #Gets user input, clears upon button press
            serial_entry=serial.get()
            serial.delete(0,END)
            tag_entry=tag.get()
            tag.delete(0,END)
            
            #Error Catch if Serial or Tag is blank, or if computer doesn't exist. else opens edit dialog
            if (serial_entry != '')and (tag_entry != ''):
                try:
                    cur.execute("SELECT * from Computers where Serial=? and Tag=?",(serial_entry,tag_entry))
                    rows = cur.fetchall()
                    checkerino=rows[0]
                    
                    global masterserial
                    masterserial = checkerino[0]                                        
                    controller.show_frame(EditEntryPage)
                except:
                    notexistEntry()
                    
            else:
                emptyEntry()

        frameTwo = tk.LabelFrame(self, text= " Menu ",font=LARGE_FONT)
        frameTwo.grid(row=0, column=9,sticky='W', \
                 padx=5, pady=5, ipadx=5, ipady=5)
        #Menu Buttons in a second frame for easy button management
        enter_button= tk.Button(frameOne, text ="Enter",command = check_entry)
        enter_button.grid(row=4,column=5)
    
        create_button = tk.Button(frameTwo, text="Create Entry",
                            command=lambda: controller.show_frame(CreatePage))
        create_button.grid(row=3,column=2)

        view_button= tk.Button(frameTwo, text="View Entry",
                               command=lambda:controller.show_frame(ViewPage))
        view_button.grid(row=4,column=2)

        return_button = tk.Button(frameTwo, text="Return To Menu",
                            command=lambda: controller.show_frame(StartPage))
        return_button.grid(row=5,column=2)
##Actual Edit Dialog. Data Entered will be changed upon user confirmation.

class EditEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #frame one for easier widget management
        frameOne = tk.LabelFrame(self, text=" Edit Entry: *Items left Blank will be Unchanged",font=LARGE_FONT)
        frameOne.grid(row=0, columnspan=5, rowspan=5,sticky='W', \
                 padx=10, pady=10, ipadx=10, ipady=10)
        #labels
        Label(frameOne,text="Tag Number").grid(row=3)
        Label(frameOne,text="Shipdate").grid(row=4)
        Label(frameOne,text="Location").grid(row=5)
        tag = Entry(frameOne)
        
        tag.grid(row=3,column=1)
        #Months Entry
        shipmonth =ttk.Combobox(frameOne,width=15)
        shipmonth['values']=months_list
        shipmonth.current(0)
        shipday=ttk.Combobox(frameOne,width=5)
        #Day Entry
        shipday['values']=days_list
        shipday.current(0)
        #Year Entry
        shipyear=ttk.Combobox(frameOne,width=5)
        shipyear['values']=years_list
        shipyear.current(0)
        #Location Entry "Floors"
        location = ttk.Combobox(frameOne,width=5)
        location['values']=locations_list
        location.current(0)
        shipmonth.grid(row=4,column=1)
        shipday.grid(row=4,column=2)
        shipyear.grid(row=4,column=3)
        location.grid(row=5,column=1)
        

        def check_entry():
            #Gets user input, clears upon button press, Executes EDIT ENTRY
            tag_entry=tag.get()
            tag.delete(0,END)
            ship_entry=shipmonth.get()+shipday.get()+shipyear.get()
            shipmonth.delete(0,END)
            shipday.delete(0,END)
            shipyear.delete(0,END)
            location_entry=location.get()
            location.delete(0,END)
            cur.execute("SELECT * FROM Computers where Serial = ?",[masterserial])
            rows= cur.fetchall()
            checkerino=rows[0]
            #If Patron leaves entry blank = NO CHANGE
            if tag_entry=='':
                tag_entry=checkerino[1]
            if ship_entry==' - '+ ' - ' + ' - ':    
                ship_entry=checkerino[2]
            if location_entry=='-':
                location_entry=checkerino[3]
            cur.execute("UPDATE Computers SET tag =?,ship=?,location=? WHERE serial=?",
                        (tag_entry,ship_entry,location_entry,masterserial))
            clickEdit()
            writeEdit(masterserial,tag_entry,ship_entry,location_entry)
            controller.show_frame(EditPage)


        enter_button= tk.Button(frameOne, text ="Enter",command = check_entry)
        enter_button.grid(row=5,column=2)



        
class ViewPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #frame one for easier widget management
        frameOne = tk.LabelFrame(self, text=" View Entry: ",font=LARGE_FONT)
        frameOne.grid(row=0, columnspan=5, rowspan=5,sticky='W', \
                 padx=10, pady=10, ipadx=10, ipady=10)
        #labels
        Label(frameOne,text="Serial Number").grid(row=2)
        Label(frameOne,text='OR').grid(row=3)
        Label(frameOne,text="Tag Number").grid(row=4)
        
        serial = Entry(frameOne)
        tag = Entry(frameOne)
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
                        for row in rows:
                            #Displays info for a single/unique computer in a popup messagebox   
                            if len(rows)==1:
                                global output
                                convert=rows[0]
                                ttserial= "Serial: "+convert[0]
                                tttag = "\nTag: " + convert[1]
                                ttship="\nShip: " + str(convert[2])
                                ttlocation="\nLocation: " +str(convert[3])
                                
                                output= ttserial+tttag+ttship+ttlocation
                                           
                                displayInfo()
                            else:
                                #Displays multiple boxes for computers with the same tag.... 
                                ttserial= "Serial: "+row[0]
                                tttag = "\nTag: " + row[1]
                                ttship="\nShip: " + str(row[2])
                                ttlocation="\nLocation: " +str(row[3])
                                output= ttserial+tttag+ttship+ttlocation
                                displayInfo()
                except:
                    notexistEntry()   
            else:
                emptyEntry()
        #Menu Buttons in a second frame for easy button management
        frameTwo = tk.LabelFrame(self, text= " Menu ",font=LARGE_FONT)
        frameTwo.grid(row=0, column=8,sticky='W', \
                 padx=5, pady=5, ipadx=5, ipady=5)
        enter_button= tk.Button(frameOne, text ="Enter",command = view_entry)
        enter_button.grid(row=4,column=2)
        create_button = tk.Button(frameTwo, text="Create Entry",
                            command=lambda: controller.show_frame(CreatePage))
        create_button.grid(row=3,column=2)
        edit_button = tk.Button(frameTwo, text="Edit Entry",
                            command=lambda: controller.show_frame(EditPage))
        edit_button.grid(row=4,column=2)
        return_button = tk.Button(frameTwo, text="Return To Menu",
                            command=lambda: controller.show_frame(StartPage))
        return_button.grid(row=5,column=2)
    


app = InventoryMGMT()
app.wm_title("Hunter College Library Systems Inventory Management")
app.mainloop()
