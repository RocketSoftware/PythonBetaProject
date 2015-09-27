"""
This MembersDemo.py program is working with UniData 8.2.0 and UniVerse 11.3.1 against XDEMO account.
Version: 1.1.0
Date: 9/2/2015

Functions:

- Find the XDEMO account path and change the working path to the XDEMO account
- This program can be running on any folder, if the account_path parameter is set in the MembersDemo.cfg file
- It requires the $UDTBIN or $UVBIN setting in the path environment variable
- Open the u2py.File("MEMBERS")
- Read the member information based on the member key id with four digit number
- Search the member based on the last name and create a selected list
- UniArray oconv / iconv on U2 date conversion
- Maintain the credit card information (working with MultiValue field)
- Input field data checking: credit card number legnth (16), security code (3), birthday format, key id (digit)
- Menu / Button state handling (NORMAL / DISABLED)
- Entry field binding with "Enter" key
- Use readnamefields function on the 'STATE' virtual field against the STATES file
- Use Subroutine function to get the address (compile & catalog GET_MEMBERS_RECORD subroutine)
- UDT _PH_ or UV &PH& directory must exist for the GET_MEMBERS_RECORD subroutine
- U2 Error handling
- Load / Save configuration file - last update MEMBER ID
- Use tkinter grid mode with menu option
- Use the Esc key or Exit button to close the Help Window (tkinter pack mode)

"""

glversion = "1.1.0"

###########
# Imports #
###########
import sys
import tkinter as tk
from tkinter import *
import datetime
from datetime import date
from tkinter import messagebox
import configparser
import xml.etree.ElementTree as ET

###############################################
# Load the MembersDemo.cfg configuration file #
###############################################

config = configparser.ConfigParser()
default_id = ""
default_u2bin = ""
default_account_path = ""
try:
    config.read('MembersDemo.cfg')
    default_setting = config['appSettings']
    try:
        default_id = default_setting['id']
    except:
        pass
    try:
        default_u2bin = default_setting['u2bin']
    except:
        pass
    try:
        default_account_path = default_setting['account_path']
    except:
        pass
except:
    pass

###############################
# Find the XDEMO account path #
###############################
import os
program_path = os.getcwd()

# Windows or UNIX environment
if program_path.find(":\\"):
    windows = True
else:
    windows = False

if default_account_path == "":
    pos = program_path.find("XDEMO")
    if pos == -1:
        print("This MembersDemo.py program is only working on the U2 XDEMO account")
        exit()
    
    # Assume the XDEMO account is installed in the UDTHOME or UVHOME folder
    
    if default_u2bin == "":
        u2bin_path = program_path[0:pos] + "bin"
    else:
        # User define the UniData or UniVerse bin path in the MembersDemo.cfg file
        # [appSettings]
        # u2bin = c:\U2\uv\bin or u2bin = c:\U2\ud82\bin
        u2bin_path = default_u2bin
    
    # If the current path is not XDEMO, please change the program path to the XDEMO account.
    
    if len(program_path) != pos + 5:
        account_path = program_path[0:pos+5]
        os.chdir(account_path)
    else:
        account_path = program_path
else:
    account_path = default_account_path
    pos = default_account_path.find("XDEMO")
    if pos == -1:
        print("This MembersDemo.py program is only working on the U2 XDEMO account")
        exit()
        
    os.chdir(account_path)
    if default_u2bin == "":
        u2bin_path = "?"
    else:
        u2bin_path = default_u2bin

# Check %UDTBIN% or %UVBIN% path setting
sys_path = sys.path
#sys_pathx = ';'.join(map(str, sys_path))

# It is case insensitive on Windows environment
if windows:
    u2bin_path_lowcase = u2bin_path.lower()
else:
    # No path change for UNIX
    u2bin_path_lowcase = u2bin_path
    
found_u2bin = False    
for item in sys_path:
    if item.lower() == u2bin_path_lowcase:
        found_u2bin = True
        break
      
if found_u2bin == False:
    u2bin_path = "?"
    print("Warning: The UDTBIN or UVBIN might not be set in the path environment variable.")
    print("UDTBIN or UVBIN = "+u2bin_path)
    print("Note: if the XDEMO account is not under UDTHOME or UVHOME folder, the UDTBIN or UVBIN path might be incorrect.")
    print("      You can set the u2bin parameter in the MembersDemo.cfg file.")

# Catch exception error, when the %UDTBIN% or %UVBIN% path setting is not in %path% variable

try:
    import u2py
except ImportError as e:
    print(e)
    exit()

##################
# GUI Properties #
##################
root = Tk()
root.configure(background = "White")
root.title("Rental Members Information System (ver: " + glversion + ")")
root.columnconfigure(0, minsize = 120)
root.columnconfigure(1, minsize = 120)
root.columnconfigure(2, minsize = 120)
root.columnconfigure(3, minsize = 120)
root.columnconfigure(4, minsize = 120)

root.resizable(width=FALSE, height=FALSE)
# root.geometry('{}x{}'.format(<widthpixels>, <heightpixels>))
# root.geometry("625x545+0+0")
w = 625
h = 545

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

#####################
# Declare Variables #
#####################
entryText = StringVar()
idText = StringVar()
lnameText = StringVar()
fnameText = StringVar()
birthdateText = StringVar()
titleText = StringVar()
cityText = StringVar()
statecodeText = StringVar()
zipText = StringVar()

homephoneText = StringVar()
genderText = StringVar()

cellphoneText = StringVar()
emailText = StringVar()
passwordText = StringVar()
imageidText = StringVar()
statusText = StringVar()
statenameText = StringVar()
addressText = StringVar()

cardnoText = StringVar()
cardexpText = StringVar()
cardnoText = StringVar()
cardsecText = StringVar()
cardtypeText = StringVar()

cardType = ""
cardNo = ""
cardExp = ""
cardSec = ""
cardIndex = 0
typeIndex = 0

#Empty dynamic array
R = u2py.DynArray()

###################
# Access U2 files #
###################
F = u2py.File("MEMBERS")

def getSelectList( thelistcommand ):
    """getSelectList( thelistcommand ) - returns selected items as pythonlist"""
    theCmd = u2py.Command("CLEARSELECT")
    theCmd = u2py.Command( thelistcommand )
    theCmd.run()
    theRtnList = []
    try:
        theList = u2py.List( 0 )
        theDynList = theList.readlist()
        #print(theDynList.count(0))
        
        for each in theDynList:
            if len(each[0]) > 0:
                theRtnList.extend( [each[0]] )

        return theRtnList
    except u2py.U2Error as e:
        return theRtnList
    
############
# Exit GUI #
############
def quitgui():
    root.destroy()

##########################
# Clean all entry fields #
##########################
def clean_fields():
    fnameText.set("")
    #lnameText.set("")
    genderText.set("")
    birthdateText.set("")
    cityText.set("")    
    statecodeText.set("")
    zipText.set("")
    homephoneText.set("")
    cellphoneText.set("")
    emailText.set("")
    passwordText.set("")
    imageidText.set("")
    statusText.set("")
    statenameText.set("")
    addressText.set("")
    list1.delete(0, END)
    
    button_Add.config(state=tk.DISABLED)
    button_Update.config(state=tk.DISABLED)
    button_Remove.config(state=tk.DISABLED)
    button_Save.config(state=tk.DISABLED)
            
    menu1.entryconfig(3, state=tk.DISABLED)
    menu1.entryconfig(4, state=tk.DISABLED)
    menu1.entryconfig(5, state=tk.DISABLED)
    menu1.entryconfig(6, state=tk.DISABLED)
    
#############################
# Search button (Member ID) #
#############################
def search():
    #Global variables we need for search
    global R
    
    label_message['text']=""
    #Reads ID entry and puts it in dynamic array
    key = entryText.get()
    if key.isdigit() == False:
       label_message['text']="Key value is not numeric"
       label_message.config(fg = "brown")
       clean_fields()
       lnameText.set("")
       return
    
    if len(key) != 4:
        key = '%0*d' % (4, int(key))
        entryText.set(key)
        
    try:
        R = F.read(key)
    except u2py.U2Error as e:
        label_message['text']=e
        label_message.config(fg = "brown")
        clean_fields()
        lnameText.set("")
        return
    
    idText.set(entryText.get())
    lnameText.set(str(R.extract(1)))
    fnameText.set(str(R.extract(2)))
    
    birthdayx=R.extract(10).oconv("D4/")
    birthdateText.set(str(birthdayx))
    
    cityText.set(str(R.extract(6)))
    statecodeText.set(str(R.extract(7)))
    zipText.set(str(R.extract(8)))
    genderText.set(str(R.extract(9)))
    
    homephoneText.set(str(R.extract(11)))
    cellphoneText.set(str(R.extract(12)))
    emailText.set(str(R.extract(13)))
    passwordText.set(str(R.extract(14)))
    imageidText.set(str(R.extract(16)))
    statusText.set(str(R.extract(17)))
    
    state_name = F.readnamedfields(key, u2py.DynArray("STATE"))
    statenameText.set(str(state_name))
    
    #Clears current listbox
    list1.delete(0, END)
    
    i = 1
    x = str(R.extract(18, i))
    while x != "":
        tdate=str(R.extract(21, i).oconv("D4/"))
        
        t = x+','+str(R.extract(20, i))+','+tdate+','+str(R.extract(22, i))
        list1.insert(i, t)
        i = i + 1
        x = str(R.extract(18, i))
    
    button_Add.config(state=tk.NORMAL)
    button_Update.config(state=tk.NORMAL)
    button_Remove.config(state=tk.NORMAL)
    button_Save.config(state=tk.NORMAL)
        
    menu1.entryconfig(3, state=tk.NORMAL)
    menu1.entryconfig(4, state=tk.NORMAL)
    menu1.entryconfig(5, state=tk.NORMAL)
    menu1.entryconfig(6, state=tk.NORMAL)
    
    label_message['text'] = "Member " + key + " data was displayed"
    label_message.config(fg = "black")
    
    # Call the GET_MEMBERS_RECORD subroutine to address
    try:
        s = u2py.Subroutine("GET_MEMBERS_RECORD", 4) 
        s.args[0] = key
        s.call()
        if str(s.args[2]) != '0':
            result="Error:"+ s.args[3]
            label_message['text']=result
            label_message.config(fg = "brown")
            return
        else:
            if len(str(s.args[1])) == 0:
                addressText.set('--- Not working ---')
                return
            
            xmlstring = s.args[1] 
    	    # print("xmlstring=", xmlstring)
    	    # Parse XML from the string into element 
            tree = ET.fromstring(xmlstring)
            for child in tree:
                if child.tag != 'ADDRESS_MV': 
                    # print(child.tag, child.text)
                    # It might be multiple addresses
                    if child.tag == "STREET_ADDRESS":
                        addressText.set(child.text)
                else:
    	            #print('STREET_ADDRESS', child.find('ADDRESS').text)
                    addressText.set(child.find('ADDRESS').text)
            
    except u2py.U2Error as e:
        label_message['text']=e
        label_message.config(fg = "brown")
        addressText.set('--- Not working ---')
        return

def keyid_enter(event):
    search()
    
#############################
# Search button (Last Name) #
#############################
def search_lname():
    # Global variables we need for search
    global R
    global u2list
    
    label_message['text']=""
    #Reads ID entry and puts it in dynamic array
    lname = lnameText.get()
    if len(lname) == 0:
       label_message['text']="The last name is not found."
       label_message.config(fg = "brown")
       return
    
    u2qry = "SSELECT MEMBERS WITH LAST_NAME = '" + lname + "'"
    
    try:
        u2list = getSelectList(u2qry)

        if len(u2list) == 0:
            label_message['text']="Could not find any record based on the last name!"
            label_message.config(fg = "brown")
            clean_fields()
            return
        else:
            if len(u2list) == 1:
                # Only one member was found based on the last name
                entryText.set(u2list[0])
                search()
                u2list.clear()
                return
        
        s = memberid_Popup()
        
        button_SearchL.config(state=tk.DISABLED)    
        menu1.entryconfig(2, state=tk.DISABLED)
        
        #Waits until addcredit_cardPopup closes before continuing
        root.wait_window(s.top)
        
        button_SearchL.config(state=tk.NORMAL)    
        menu1.entryconfig(2, state=tk.NORMAL)
    
        # if key id was selected
        if s.idselected:
            entryText.set(s.id)
            search()
            
            u2list.clear()
            label_message['text'] = "Member " + s.id + " data was displayed" 
            label_message.config(fg = "black")
        
    except u2py.U2Error as e:
        label_message['text']="Error:" + e
        label_message.config(fg = "brown")
        return
 
class memberid_Popup(object):
    global u2list
    def __init__(self):
        
        # Create the popup window with set configurations
        top=self.top=Toplevel()
        top.configure(background = "white")
        top.geometry("300x160")
        top.resizable(width=FALSE, height=FALSE)
        top.columnconfigure(0, minsize = 130)
        top.columnconfigure(1, minsize = 130)
         
        self.l=Label(top,text="ID list (last name):", fg = "blue", bg = "white", font = ("Verdana", 10))
        self.l.grid(row = 0, column = 0, pady = (10, 0))
        self.lname=Label(top,text=lnameText.get(), fg = "blue", bg = "white", font = ("Verdana", 10))
        self.lname.grid(row = 0, column = 1, pady = (10, 0), sticky=W)
         
        self.lb=Listbox(top, width = 15, height=6, selectmode = SINGLE, fg = "blue", bg = "white", font = ("Verdana", 10))
        self.lb.grid(row = 1, column = 0, rowspan = 6,  padx = (5, 5))
        
        self.lb.bind("<Button-1>", self.callback)
        #self.lb.bind("<Escape>", self.quitselect)
         
        for id in u2list:
            self.lb.insert(END, id)
        
        self.b=Button(top,text='Choose Member ID',command=self.cleanup, fg = "blue", bg = "white", font = ("Verdana", 10), width = 18)
        self.b.grid(row = 4, column = 1, pady = 10)
        self.b=Button(top,text='Quit',command=self.quitselect, fg = "blue", bg = "white", font = ("Verdana", 10), width = 18)
        self.b.grid(row = 5, column = 1, pady = 10)
        
        self.message = Label(top, text = "", fg = "brown", bg = "white", font = ("Verdana", 10), width=30)
        self.message.grid(row = 8, column = 0, columnspan = 2, padx = 2, pady = 2, sticky = SW)

    def cleanup(self):
        # Sets value to currently selected credit_card
        self.message['text'] = ""
        try:
            idIndex = self.lb.curselection()[0]
            self.id= self.lb.get(idIndex)

        except IndexError:
            # self.messageWindowx("No credit card type was selected.")
            self.message['text'] = "Please select the MEMBER ID"
            return
            
        self.idselected = True
        # Destroy popup window
        self.top.destroy()
        
    def quitselect(self):
        self.idselected = False
        
        # Destroy popup window
        self.top.destroy()
        
    def callback(self, event=None):
        # self.cleanup()
        self.message['text'] = ""
        try:
            idIndex = self.lb.curselection()[0]
            self.id= self.lb.get(idIndex)
        except IndexError:
            self.message['text'] = "Please select the MEMBER ID"
            return
	            
        self.idselected = True
        # Destroy popup window
        self.top.destroy()
     
###################
# Add Credit Card #
###################
def addcredit_card():
    
    # Global variables we need
    global R
    
    label_message['text']=""
    # Opens addcredit_cardPopup credit_card and access its variables using c
    c = addcredit_cardPopup()
    
    button_Search.config(state=tk.DISABLED)
    button_Add.config(state=tk.DISABLED)
    button_Update.config(state=tk.DISABLED)
    button_Remove.config(state=tk.DISABLED)
    button_Save.config(state=tk.DISABLED)
    
    menu1.entryconfig(3, state=tk.DISABLED)
    menu1.entryconfig(4, state=tk.DISABLED)
    menu1.entryconfig(5, state=tk.DISABLED)
    menu1.entryconfig(6, state=tk.DISABLED)

    label_message['text']="* Add a credit card *"
    label_message.config(fg = "black")
    
    # Waits until addcredit_cardPopup closes before continuing
    root.wait_window(c.top)
    
    button_Search.config(state=tk.NORMAL)
    button_Add.config(state=tk.NORMAL)
    button_Update.config(state=tk.NORMAL)
    button_Remove.config(state=tk.NORMAL)
    button_Save.config(state=tk.NORMAL)
    
    menu1.entryconfig(3, state=tk.NORMAL)
    menu1.entryconfig(4, state=tk.NORMAL)
    menu1.entryconfig(5, state=tk.NORMAL)
    menu1.entryconfig(6, state=tk.NORMAL)
    
    label_message['text']=""

    if c.add == False:
        return
    
    t = c.cardno+','+c.cardtype+','+c.cardexp+','+c.cardsec
    list1.insert(END, t)
    lsize=list1.size()
    
    R.insert(18, lsize, c.cardno)
    R.insert(20, lsize, c.cardtype)
    
    tdate=u2py.DynArray(c.cardexp)
    cardexpx=tdate.iconv("D4/")
    
    R.insert(21, lsize, cardexpx)
    R.insert(22, lsize, c.cardsec)
            
    F.write(entryText.get(), R)
    
class addcredit_cardPopup(object):
    def __init__(self):
        
        # Creates the popup window with set configurations
        top=self.top=Toplevel()
        top.configure(background = "white")
        top.geometry("300x220")
        top.resizable(width=FALSE, height=FALSE)
        top.columnconfigure(0, minsize = 150)
        top.columnconfigure(1, minsize = 150)
        
        self.add = False
        self.l=Label(top,text="Credit Card Type:", fg = "blue", bg = "white", font = ("Verdana", 10))
        self.l.grid(column = 0, row = 0, pady = (10, 0))
        
        # Use ListBox to select the credit card type
        
        # Creates a listbox for list of Credit Card
        # self.lb=Listbox(top, width = 15, height=3, selectmode = SINGLE, fg = "blue", bg = "white", font = ("Verdana", 10))
        # self.lb.grid(row = 1, column = 0, rowspan = 3,  padx = (0, 5))
        # self.lb.insert(END, "AMEX")
        # self.lb.insert(END, "MC")
        # self.lb.insert(END, "V")
        
        # Use DropdownBox to select the credit card type
        
        self.ochoices = ("AMEX", "MC", "V")
        self.otype = StringVar()
        self.otype.set(self.ochoices[0])
        self.o = OptionMenu(top, self.otype, *self.ochoices)
	        
        self.o['menu'].config(bg = "white")
        self.o.config(bg = "white", font = ("Verdana", 10), width = 6)
        self.o.grid(row = 1, column = 0, pady = 10)
        
        self.l2=Label(top,text="Card Number:", fg = "blue", bg = "white", font = ("Verdana", 10))
        self.l2.grid(row = 2, column = 0, padx = (0, 10), pady = (10, 0))
        self.data_cardno = Entry(top, textvariable = cardnoText, bg = "white", font = ("Verdana", 10), width = 16)
        self.data_cardno.grid(row = 3, column = 0, pady = (10, 0), sticky = W)
        
        self.l3=Label(top,text="Card Expired:", fg = "blue", bg = "white", font = ("Verdana", 10))
        self.l3.grid(row = 0, column = 1, padx = (0, 10), pady = (10, 0))
        self.data_cardexp = Entry(top, textvariable = cardexpText, bg = "white", font = ("Verdana", 10), width = 16)
        self.data_cardexp.grid(row = 1, column = 1, pady = (10, 0), sticky = W)
        
        self.l4=Label(top,text="Security Code:", fg = "blue", bg = "white", font = ("Verdana", 10))
        self.l4.grid(row = 2, column = 1, padx = (0, 10), pady = (10, 0))
        self.data_cardsec = Entry(top, textvariable = cardsecText, bg = "white", font = ("Verdana", 10), width = 16)
        self.data_cardsec.grid(row = 3, column = 1, pady = (10, 0), sticky = W)
        
        # Creates the two buttons, one for adding the Credit Card, one for showing more info
        # Add Credit Card goes to cleanup function and More Info goes to moreinfo function
        
        self.b=Button(top,text='Add Credit Card',command=self.cleanup, fg = "blue", bg = "white", font = ("Verdana", 10), width = 16)
        self.b.grid(row = 5, column = 0, pady = 10, sticky = W)
        self.b=Button(top,text='Quit',command=self.quitadd, fg = "blue", bg = "white", font = ("Verdana", 10), width = 16)
        self.b.grid(row = 5, column = 1, pady = 10, sticky = W)

    def cleanup(self):
        # Sets value to currently selected Credit Card and value2 to selected grade

        # Use the ListBox
        # self.cardtype=self.lb.get(ACTIVE)
        # try:
        #    cardIndex = self.lb.curselection()[0]
        #    self.cardtype = self.lb.get(cardIndex)
        # except IndexError:
        #    self.messageWindowx("No credit card type was selected.")
        #    return
            
        self.cardtype = self.otype.get()
        
        self.cardno=self.data_cardno.get()
        if len(self.cardno) < 16:
            self.messageWindowx("Credit card number is too short.")
            return
        
        self.cardsec=self.data_cardsec.get()
        if len(self.cardsec) != 3:
            self.messageWindowx("Credit card sec code is not 3 number.")
            return
        
        self.cardexp=self.data_cardexp.get()
        try:
            datetime.datetime.strptime(self.cardexp, '%m/%d/%Y')
        except ValueError:
            self.messageWindowx("Incorrect date format, should be MM/DD/YYYY")
            return
        
        self.add = True
        # Destroy popup window
        self.top.destroy()
        
    def quitadd(self):
        self.add = False
        # Destroy popup window
        self.top.destroy()
        
    def messageWindowx(self, msg):
        win = Toplevel()
        win.title('Credit card')
        win.config(background= "white")
        win.geometry("240x100")
        message = msg
        Label(win, text=message, bg = "white", fg = "blue", font = ("Verdana", 10)).pack(pady = 10)
        Button(win, text='Ok', command=win.destroy, bg = "white", fg = "blue", font = ("Verdana", 10), width = 10).pack(pady = 10)
    
######################
# Change Credit Card #
######################
def changecredit_card():
    # Global variable we need
    global R

    label_message['text']=""
    if list1.size()==0:
        messageWindow1()
        return
    
    # Sets findcredit_card to currently selected credit_card
    # findcredit_card = list1.get(ACTIVE)
    
    try:
        cardIndex = list1.curselection()[0]
        findcredit_card = list1.get(cardIndex)
    except IndexError:
        messageWindow1()
        return
    
    # Parser the string to four fiedls
    j = findcredit_card.find(',')
    cardNo=findcredit_card[:j]
    findcredit_card=findcredit_card[j+1:]
    j = findcredit_card.find(',')
    cardType=findcredit_card[:j]
    
    findcredit_card=findcredit_card[j+1:]
    j = findcredit_card.find(',')
    cardExp=findcredit_card[:j]
    cardSec=findcredit_card[j+1:]
    
    cardnoText.set(cardNo)
    cardexpText.set(cardExp)
    cardsecText.set(cardSec)
    cardtypeText.set(cardType)
    
    # Opens changecredit_cardPopup credit_card and access its variables using g
    g = changecredit_cardPopup()

    button_Search.config(state=tk.DISABLED)
    button_Add.config(state=tk.DISABLED)
    button_Update.config(state=tk.DISABLED)
    button_Remove.config(state=tk.DISABLED)
    button_Save.config(state=tk.DISABLED)
    
    menu1.entryconfig(3, state=tk.DISABLED)
    menu1.entryconfig(4, state=tk.DISABLED)
    menu1.entryconfig(5, state=tk.DISABLED)
    menu1.entryconfig(6, state=tk.DISABLED)
    label_message['text']="* Update credit card *"
    label_message.config(fg = "black")
    
    # Waits until changecredit_cardPopup closes before continuing
    root.wait_window(g.top)
    
    button_Search.config(state=tk.NORMAL)
    button_Add.config(state=tk.NORMAL)
    button_Update.config(state=tk.NORMAL)
    button_Remove.config(state=tk.NORMAL)
    button_Save.config(state=tk.NORMAL)
    
    menu1.entryconfig(3, state=tk.NORMAL)
    menu1.entryconfig(4, state=tk.NORMAL)
    menu1.entryconfig(5, state=tk.NORMAL)
    menu1.entryconfig(6, state=tk.NORMAL)
    
    label_message['text']=""
    if g.change == False:
        return
    
    # Pass self.values back to here
    R.replace(18, cardIndex+1, g.cardno)
    R.replace(20, cardIndex+1, g.cardtype)
    
    tdate=u2py.DynArray(g.cardexp)
    cardexpx=tdate.iconv("D4/")
    
    R.replace(21, cardIndex+1, cardexpx)
    R.replace(22, cardIndex+1, g.cardsec)
    
    # Overwrites the current member's entry in the MEMBERS file with the Dynamic Array
    F.write(entryText.get(), R)
    
    out=g.cardno+','+g.cardtype+','+g.cardexp+','+g.cardsec
    try:
        list1.delete(cardIndex)
    except IndexError:
        cardIndex = tk.END
            
    # Insert edited item back into listbox at index
    list1.insert(cardIndex, out)
    
def messageWindow1():
    win = Toplevel()
    win.title('Credit card')
    win.config(background= "white")
    win.geometry("240x100")
    message = "No active credit card was found."
    Label(win, text=message, bg = "white", fg = "blue", font = ("Verdana", 10)).pack(pady = 10)
    Button(win, text='Ok', command=win.destroy, bg = "white", fg = "blue", font = ("Verdana", 10), width = 10).pack(pady = 10)
    
class changecredit_cardPopup(object):
    # Global variable we need
    
    def __init__(self):
        
        #Creates the popup window with set configurations
        top=self.top=Toplevel()
        top.configure(background = "white")
        top.geometry("300x220")
        top.resizable(width=FALSE, height=FALSE)
        top.columnconfigure(0, minsize = 150)
        top.columnconfigure(1, minsize = 150)
	
        self.change = False
        self.l=Label(top,text="Credit Card Type:", fg = "blue", bg = "white", font = ("Verdana", 10))
        self.l.grid(column = 0, row = 0, pady = (10, 0))
	        
        self.lb=Listbox(top, width = 15, height=3, selectmode = SINGLE, fg = "blue", bg = "white", font = ("Verdana", 10))
	        
        # Create a listbox for list of Credit Card
        self.lb.grid(row = 1, column = 0, rowspan = 3,  padx = (0, 5))
	
        cardType=cardtypeText.get()
        card_choice=0
        self.lb.insert(END, "AMEX")
        if cardType == "AMEX":
            #self.lb.activate(0)
            card_choice=0
            
        self.lb.insert(END, "MC")
        if cardType == "MC":
            # self.lb.activate(1)
            card_choice=1
            
        self.lb.insert(END, "V")
        if cardType == "V":
            # self.lb.activate(2)
            card_choice=2
	
        self.lb.select_set(card_choice)
        self.lb.event_generate("<<ListboxSelect>>")
	
        self.l2=Label(top,text="Card Number:", fg = "blue", bg = "white", font = ("Verdana", 10))
        self.l2.grid(row = 5, column = 0, padx = (0, 10), pady = (10, 0))
        self.data_cardno = Entry(top, textvariable = cardnoText, bg = "white", font = ("Verdana", 10), width = 16)
        self.data_cardno.grid(row = 6, column = 0, pady = (10, 0), sticky = W)
	        
        self.l3=Label(top,text="Card Expired:", fg = "blue", bg = "white", font = ("Verdana", 10))
        self.l3.grid(row = 0, column = 1, padx = (0, 10), pady = (10, 0))
        self.data_cardexp = Entry(top, textvariable = cardexpText, bg = "white", font = ("Verdana", 10), width = 16)
        self.data_cardexp.grid(row = 1, column = 1, pady = (10, 0), sticky = W)
	        
        self.l4=Label(top,text="Security Code:", fg = "blue", bg = "white", font = ("Verdana", 10))
        self.l4.grid(row = 2, column = 1, padx = (0, 10), pady = (10, 0))
        self.data_cardsec = Entry(top, textvariable = cardsecText, bg = "white", font = ("Verdana", 10), width = 16)
        self.data_cardsec.grid(row = 3, column = 1, pady = (10, 0), sticky = W)
	        
        # Create the two buttons, one for adding the credit_card, one for showing more info
        # Add Credit Card goes to cleanup function and More Info goes to moreinfo function
	        
        self.b=Button(top,text='Update Credit Card',command=self.cleanup, fg = "blue", bg = "white", font = ("Verdana", 10), width = 16)
        self.b.grid(row = 5, column = 1, pady = 10, sticky = W)
        
        self.b=Button(top,text='Quit',command=self.quitchange, fg = "blue", bg = "white", font = ("Verdana", 10), width = 16)
        self.b.grid(row = 6, column = 1, pady = 10, sticky = W)
        
    def cleanup(self):
        try:
            # self.cardtype = self.lb.get(ACTIVE)
            typeIndex = self.lb.curselection()[0]
            self.cardtype = self.lb.get(typeIndex)
            
        except IndexError:
            self.messageWindowx("No active credit card type was found.")
            return
 
        self.cardno=self.data_cardno.get()
        if len(self.cardno) < 16:
            self.messageWindowx("credit card number is too short.")
            return
        
        self.cardsec=self.data_cardsec.get()
        if len(self.cardsec) != 3:
           self.messageWindowx("credit card sec code is not 3 number.")
           return
	        
        self.cardexp=self.data_cardexp.get()
        try:
           datetime.datetime.strptime(self.cardexp, '%m/%d/%Y')
        except ValueError:
            self.messageWindowx("Incorrect data format, should be MM/DD/YYYY")
            return
            
        self.change=True
        # Destroys popup window
        self.top.destroy()
        
    def quitchange(self):
        # Destroys popup window
        self.change=False
        self.top.destroy()
        
    def messageWindowx(self, msg):
        win = Toplevel()
        win.title('Credit card')
        win.config(background= "white")
        win.geometry("240x100")
        message = msg
        Label(win, text=message, bg = "white", fg = "blue", font = ("Verdana", 10)).pack(pady = 10)
        Button(win, text='Ok', command=win.destroy, bg = "white", fg = "blue", font = ("Verdana", 10), width = 10).pack(pady = 10)

######################
# Remove Credit Card #
######################
def removecredit_card():
    global R
    # Global Variables we need
    
    label_message['text']=""
    # findcredit_card = list1.get(ACTIVE)
    # Sets findcredit_card to currently selected Credit Card
    
    if list1.size()==0:
        messageWindow1()
        return
        
    # Sets findcredit_card to currently selected Credit Card
    # findcredit_card = list1.get(ACTIVE)
    
    try:
        cardIndex = list1.curselection()[0]
        # print(cardIndex) - 0, 1,2,3
        findcredit_card = list1.get(cardIndex)
    except IndexError:
        messageWindow1()
        return
    
    button_Search.config(state=tk.DISABLED)
    button_Add.config(state=tk.DISABLED)
    button_Update.config(state=tk.DISABLED)
    button_Remove.config(state=tk.DISABLED)
    button_Save.config(state=tk.DISABLED)
    
    menu1.entryconfig(3, state=tk.DISABLED)
    menu1.entryconfig(4, state=tk.DISABLED)
    menu1.entryconfig(5, state=tk.DISABLED)
    menu1.entryconfig(6, state=tk.DISABLED)

    label_message['text']="* Remove a credit card *"
    label_message.config(fg = "black")
    
    choice=messagebox.askokcancel("Credit Card","Delete the '"+findcredit_card+"' credit card?")
    
    button_Search.config(state=tk.NORMAL)
    button_Add.config(state=tk.NORMAL)
    button_Update.config(state=tk.NORMAL)
    button_Remove.config(state=tk.NORMAL)
    button_Save.config(state=tk.NORMAL)
    
    menu1.entryconfig(3, state=tk.NORMAL)
    menu1.entryconfig(4, state=tk.NORMAL)
    menu1.entryconfig(5, state=tk.NORMAL)
    menu1.entryconfig(6, state=tk.NORMAL)
    label_message['text']=""
    if choice == False:
        return
    
    R.delete(18, cardIndex+1)
    R.delete(20, cardIndex+1)
    R.delete(21, cardIndex+1)
    R.delete(22, cardIndex+1)
        
    # Overwrites the current member's entry in the MEMBERS file with the Dynamic Array
    F.write(entryText.get(), R)
    
    # Deletes current selection from the listbox
    list1.delete(cardIndex, cardIndex)
    
################
# Save Changes #
################
def savechanges():

    label_message['text']=""
    # Replaces Dynamic Array content with ones in the entry
    choice=messagebox.askokcancel("Member infomation","Update the member '"+entryText.get()+"' information?")
    if choice == False:
        return
    
    try:
        datetime.datetime.strptime(birthdateText.get(), '%m/%d/%Y')
    except ValueError:
        label_message['text'] = "Incorrect birthday date format, should be MM/DD/YYYY"
        label_message.config(fg = "brown")
        return
        
    R.replace(1, lnameText.get())
    R.replace(2, fnameText.get())
    
    R.replace(6, cityText.get())
    R.replace(7, statecodeText.get())
    R.replace(8, zipText.get())
    R.replace(9, genderText.get())
    
    birthdayx = u2py.DynArray(birthdateText.get()).iconv("D4/")
    R.replace(10, str(birthdayx))
    
    R.replace(11, homephoneText.get())
    R.replace(12, cellphoneText.get())
    R.replace(13, emailText.get())
    R.replace(14, passwordText.get())
    R.replace(16, imageidText.get())
    R.replace(17, statusText.get())
    
    # Overwrites the current member's entry in the MEMBERS file with the Dynamic Array
    F.write(entryText.get(), R)
    
    # Popupwindow confirming changes
    # messageWindow()
    label_message['text'] = "Member " + entryText.get() + " information was saved successfully!"
    label_message.config(fg = "black")

def messageWindow():

    win = Toplevel()
    win.title('Save changes Successfully')
    win.config(background= "white")
    win.geometry("240x100")
    message = "Your file was successfully saved."
    Label(win, text=message, bg = "white", fg = "blue", font = ("Verdana", 10)).pack(pady = 10)
    Button(win, text='Ok', command=win.destroy, bg = "white", fg = "blue", font = ("Verdana", 10), width = 10).pack(pady = 10)

########
# Quit #
########
def quittest():
    try:
        # Change back to the program path and create the MembersDemo.cfg configuration file in that folder
        os.chdir(program_path)
        config = configparser.ConfigParser()
        config['appSettings'] = {}
        config['appSettings']['id'] = entryText.get()
        if default_u2bin != "":
            config['appSettings']['u2bin'] = u2bin_path
        if default_account_path != "":
            config['appSettings']['account_path'] = default_account_path
        with open('MembersDemo.cfg', 'w') as configfile:
            config.write(configfile)
    except:
        pass
    
    root.destroy()
    #Exits the GUI window

########
# Help #
########
def help_function():
    # Opens a help window
    menu2.entryconfig(1, state=tk.DISABLED)
    h = help_Popup()
    
    # Waits until help_Popup closes before continuing
    # root.wait_window(h)

class help_Popup(object):
    def __init__(self):
        # Create the popup window with set configurations
        top=self.top=Toplevel()
        top.configure(background = "white")
        top.geometry("1100x310")

        top.title("U2 MembersDemo - Help")

        top.protocol("WM_DELETE_WINDOW", top.iconify)
        top.bind('<Escape>', lambda e: top.destroy())
        
        self.S = Scrollbar(top)
        self.S.pack(side=RIGHT, fill=Y)
        
        self.T = Text(top, height=19, width=120)
        self.T.pack(side=LEFT, fill=Y)
        self.S.config(command=self.T.yview)
        self.T.config(yscrollcommand=self.S.set)

        quote = """Functions:
        - Find the XDEMO account path and change the working path to the XDEMO account
        - This program can be running on any folder, if the account_path parameter is set in the MembersDemo.cfg file
        - It requires the $UDTBIN or $UVBIN setting in the path environment variable
        - Open the u2py.File("MEMBERS")
	- Read the member information based on the member key id with four digit number
	- Search the member based on the last name and create a selected list
	- UniArray oconv / iconv on U2 date conversion
	- Maintain the credit card information (working with MultiValue field)
	- Input field data checking: credit card number legnth (16), security code (3), birthday format, key id (digit)
	- Menu / Button state handling (NORMAL / DISABLED)
	- Entry field binding with "Enter" key
	- Use readnamefields function on the 'STATE' virtual field against the STATES file
	- Use Subroutine function to get the address (compile & catalog GET_MEMBERS_RECORD subroutine)
	- UDT _PH_ or UV &PH& directory must exist for the GET_MEMBERS_RECORD subroutine
	- U2 Error handling
	- Load / Save configuration file - last update MEMBER ID
        - Use tkinter grid mode with menu option
        - Use the Esc key or Exit button to close the Help Window (tkinter pack mode)"""
        self.T.insert(END, quote)
        
        self.B=Button(top,text='Exit',command=self.cleanup, fg = "blue", bg = "white", font = ("Verdana", 10), width = 16)
        self.B.pack(side=BOTTOM)
        return
 
    def cleanup(self):
        menu2.entryconfig(1, state=tk.NORMAL)
        self.top.destroy()

# An optional step to create the Rocket label and the blue background
# Only GIF or PNG images are accepted
# canvas
canvas1 = Canvas(root, height = 100, bg = "blue", width = 800)
canvas1.grid(row = 0, column = 0, columnspan = 10)
# image1 = PhotoImage(file = "logo.gif")
# label_image1 = Label(root, image = image1, height=100)
# label_image1.grid(row = 0,column=0, columnspan = 5, padx = 50, sticky=W)
label_rocket = Label(text = "Rocket U2 Python", fg = "blue", bg = "white", font = ("Verdana", 20))
label_rocket.grid(row = 0,column=0, columnspan = 5, padx = 50, sticky=W)

# This is how you create the menu bar in TKinter
# The only relevant option was Quit for me but you can add anything other function you want

menubar = Menu(root, tearoff= 0)
menu1 = Menu(menubar)
menu1.add_command(label = "Member Info (ID)", command = search)
menu1.add_command(label = "Search (Last Name)", command = search_lname)

menu1.add_command(label = "Add Credit Card", command = addcredit_card)
menu1.add_command(label = "Update Credit Card", command = changecredit_card)
menu1.add_command(label = "Remove Credit Card", command = removecredit_card)
menu1.add_command(label = "Save Member Info", command = savechanges)
menu1.add_separator()
menu1.add_command(label = "Quit", command = quittest)
menu1.entryconfig(3, state=tk.DISABLED)
menu1.entryconfig(4, state=tk.DISABLED)
menu1.entryconfig(5, state=tk.DISABLED)
menu1.entryconfig(6, state=tk.DISABLED)
menubar.add_cascade(label = "File", menu = menu1)

menu2 = Menu(menubar)
menu2.add_command(label = "Help", command = help_function)
menubar.add_cascade(label = "Help", menu = menu2)

root.config(menu = menubar)

# input key id value and enter

label_id = Label(text = "Members ID:", fg = "blue", bg = "white", font = "Verdana")
label_id.grid(row = 5, column = 0, pady = (10,5), columnspan = 1, sticky = W)
entry_id = Entry(root, textvariable = entryText, font = "Verdana", width = 14)
entry_id.grid(row = 5, column = 1, pady = (10,5), sticky = W)

entry_id.bind('<Return>', keyid_enter)

if default_id == "":
    entryText.set('0133')
else:
    entryText.set(default_id)

# Buttons setting

button_Search = Button(root, text = "Member Info (ID)", command = search, fg = "blue", bg = "white", font = ("Verdana", 10), width = 18)
button_Search.grid(row = 5, column = 2, pady = (10,10), sticky = W)
button_SearchL = Button(root, text = "Search (Last Name)", command = search_lname, fg = "blue", bg = "white", font = ("Verdana", 10), width = 18)
button_SearchL.grid(row = 5, column = 3, pady = (10,10), sticky = W)

button_Add = Button(root, text = "Add Credit Card", command = addcredit_card, fg = "blue", bg = "white", font = ("Verdana", 10), width = 18)
button_Add.grid(row = 18, column = 2, pady = (10, 10), sticky = NW)
button_Save = Button(root, text = "Save Changes", command = savechanges, fg = "blue", bg = "white", font = ("Verdana", 10), width = 18)
button_Save.grid(row = 18, column = 3, pady = 10, sticky = NW)

button_Update = Button(root, text = "Update Credit Card", command = changecredit_card, fg = "blue", bg = "white", font = ("Verdana", 10), width = 18)
button_Update.grid(row = 19, column = 2, pady = 10, sticky = NW)
button_Remove = Button(root, text = "Remove Credit Card", command = removecredit_card, fg = "blue", bg = "white", font = ("Verdana", 10), width = 18)
button_Remove.grid(row = 19, column = 3, pady = 10, sticky = NW)

button_Quit = Button(root, text = "Quit", command = quittest, fg = "blue", bg = "white", font = ("Verdana", 10), width = 18)
button_Quit.grid(row = 20, column = 3, pady = 10, sticky = W)

label_fname = Label(text = "First Name:", fg = "blue", bg = "white", font = ("Verdana", 10))
label_fname.grid(row = 10, column = 0, pady = 5, sticky = W)
data_fname = Entry(root, textvariable = fnameText, bg = "white", font = ("Verdana", 10), width = 18)
data_fname.grid(row = 10, column = 1, pady = 5, sticky = W)

label_lname = Label(text = "Last Name:", fg = "blue", bg = "white", font = ("Verdana", 10))
label_lname.grid(row = 10, column = 2, pady = 5, sticky = W)
data_lname = Entry(root, textvariable = lnameText, bg = "white", font = ("Verdana", 10), width = 18)
data_lname.grid(row = 10, column = 3,  pady = 5, sticky = W)
label_gender = Label(text = "Gender:", fg = "blue", bg = "white", font = ("Verdana", 10))
label_gender.grid(row = 11, column = 0, pady = 5, sticky = W)
data_gender = Entry(root, textvariable = genderText, bg = "white", font = ("Verdana", 10), width = 18)
data_gender.grid(row = 11, column = 1, pady = 5, sticky = W)
label_birthdate = Label(text = "Birth date:", fg = "blue", bg = "white", font = ("Verdana", 10))
label_birthdate.grid(row = 11, column = 2, pady = 5, sticky = W)
data_birthdate = Entry(root, textvariable = birthdateText, bg = "white", font = ("Verdana", 10), width = 18)
data_birthdate.grid(row = 11, column = 3, pady = 5, sticky = W)
label_city = Label(text = "City:", fg = "blue", bg = "white", font = ("Verdana", 10))
label_city.grid(row = 12, column = 0, pady = 5, sticky = W)
data_city = Entry(root, textvariable = cityText, bg = "white", font = ("Verdana", 10), width = 18)
data_city.grid(row = 12, column = 1, pady = 5, sticky = W)

labe_homephone = Label(text = "Home Phone:", fg = "blue", bg = "white", font = ("Verdana", 10))
labe_homephone.grid(row = 12, column = 2, pady = 5, sticky = W)
data_homephone = Entry(root, textvariable = homephoneText, bg = "white", font = ("Verdana", 10), width = 18)
data_homephone.grid(row = 12, column = 3, pady = 5, sticky = W)
labe_cellphone = Label(text = "Cell Phone:", fg = "blue", bg = "white", font = ("Verdana", 10))
labe_cellphone.grid(row = 13, column = 2, pady = 5, sticky = W)
data_cellphone = Entry(root, textvariable = cellphoneText, bg = "white", font = ("Verdana", 10), width = 18)
data_cellphone.grid(row = 13, column = 3, pady = 5, sticky = W)

label_statecode = Label(text = "State Code:", fg = "blue", bg = "white", font = ("Verdana", 10))
label_statecode.grid(row = 13, column = 0, pady = 5, sticky = W)
data_cellphone = Entry(root, textvariable = statecodeText, bg = "white", font = ("Verdana", 10), width = 18)
data_cellphone.grid(row = 13, column = 1, pady = 5, sticky = W)
labe_zip = Label(text = "Zip:", fg = "blue", bg = "white", font = ("Verdana", 10))
labe_zip.grid(row = 14, column = 0, pady = 5, sticky = W)
data_zip = Entry(root, textvariable = zipText, bg = "white", font = ("Verdana", 10), width = 18)
data_zip.grid(row = 14, column = 1, pady = 5, sticky = W)

labe_email = Label(text = "Email:", fg = "blue", bg = "white", font = ("Verdana", 10))
labe_email.grid(row = 14, column = 2, pady = 5, sticky = W)
data_email = Entry(root, textvariable = emailText, bg = "white", font = ("Verdana", 10), width = 18)
data_email.grid(row = 14, column = 3, pady = 5, sticky = W)

labe_password = Label(text = "Password:", fg = "blue", bg = "white", font = ("Verdana", 10))
labe_password.grid(row = 15, column = 0, pady = 5, sticky = W)
data_password = Entry(root, textvariable = passwordText, bg = "white", font = ("Verdana", 10), width = 18)
data_password.grid(row = 15, column = 1, pady = 5, sticky = W)
labe_imageid = Label(text = "Image ID:", fg = "blue", bg = "white", font = ("Verdana", 10))
labe_imageid.grid(row = 15, column = 2, pady = 5, sticky = W)
data_imageid = Entry(root, textvariable = imageidText, bg = "white", font = ("Verdana", 10), width = 18)
data_imageid.grid(row = 15, column = 3, pady = 5, sticky = W)
labe_status = Label(text = "Status:", fg = "blue", bg = "white", font = ("Verdana", 10))
labe_status.grid(row = 16, column = 0, pady = 5, sticky = W)
data_status = Entry(root, textvariable = statusText, bg = "white", font = ("Verdana", 10), width = 18)
data_status.grid(row = 16, column = 1, pady = 5, sticky = W)

labe_statename = Label(text = "State Name (Virtual):", fg = "blue", bg = "white", font = ("Verdana", 10))
labe_statename.grid(row = 16, column = 2, pady = 5, sticky = W)
data_statename = Entry(root, textvariable = statenameText, bg = "white", font = ("Verdana", 10), width = 18)
data_statename.grid(row = 16, column = 3, pady = 5, sticky = W)
data_statename.config(state=tk.DISABLED)

labe_address = Label(text = "Address (Subroutine):", fg = "blue", bg = "white", font = ("Verdana", 10))
labe_address.grid(row = 17, column = 2, pady = 5, sticky = W)
data_address = Entry(root, textvariable = addressText, bg = "white", font = ("Verdana", 10), width = 18)
data_address.grid(row = 17, column = 3, pady = 5, sticky = W)
data_address.config(state=tk.DISABLED)

# The listbox is for multiple credit cards

labe_creditcard = Label(text = "Credit Card:", fg = "blue", bg = "white", font = ("Verdana", 10)).grid(row = 17, column = 0, sticky = W)
list1 = Listbox(root, width = 35, height = 5, selectmode = SINGLE, bg = "white", font = ("Verdana", 10))
list1.grid(row = 18, column = 0, rowspan = 5, pady = (5,0), columnspan = 2, sticky = NW)

label_message = Label(text = "", fg = "blue", bg = "white", font = ("Verdana", 10), width=45)
label_message.grid(row = 20, column = 0, columnspan = 3, pady = 5, sticky = W)

button_Add.config(state=tk.DISABLED)
button_Update.config(state=tk.DISABLED)
button_Remove.config(state=tk.DISABLED)
button_Save.config(state=tk.DISABLED)

label_message['text'] = "Python version: "+ str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + ", U2 bin Path= " + u2bin_path

root.mainloop()
