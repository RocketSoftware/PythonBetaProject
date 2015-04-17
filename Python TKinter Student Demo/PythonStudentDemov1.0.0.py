###########
# Imports #
###########
import sys
import u2py
import tkinter as tk
from tkinter import *

##################
# GUI Properties #
##################
root = Tk()
root.geometry("600x500+0+0")
root.configure(background = "White")
root.title("Student Information Manager")
root.columnconfigure(0, minsize = 120)
root.columnconfigure(1, minsize = 120)
root.columnconfigure(2, minsize = 120)
root.columnconfigure(3, minsize = 120)
root.columnconfigure(4, minsize = 120)

#####################
# Declare Variables #
#####################
entryText = StringVar()
idText = StringVar()
fnameText = StringVar()
lnameText = StringVar()
majorText = StringVar()
minorText = StringVar()
advisorText = StringVar()
semesterText = StringVar()
classType = ""
i = 1
#Semester tracker
k = 1
#Class tracker
R = u2py.DynArray()
#Empty dynamic array

########################
# Access UniData files #
########################
F = u2py.File("STUDENT")
F2 = u2py.File("COURSES")
T = u2py.DynArray("TEACHERS")

############
# Exit GUI #
############
def quitgui():
    root.destroy()

#################
# Search button #
#################
def search():
    
    global i, k, R
    #Global variables we need for search
    
    R = F.read(entryText.get())
    #Reads ID entry and puts it in dynamic array
    
    idText.set(entryText.get())
    fnameText.set(str(R.extract(2)))
    lnameText.set(str(R.extract(1)))
    majorText.set(str(R.extract(3)))
    minorText.set(str(R.extract(4)))
    advisorText.set(str(R.extract(5)))
    semesterText.set(str(R.extract(6, 1)))
    #Extracts from the file and sets corresponding entries
    
    w['menu'].delete(0, "end")
    semesterChoices = []
    #Clears current choices in semester drop menu
    
    x = str(R.extract(6, i))
    while x != "":
        semesterChoices.insert(i, str(R.extract(6, i)))
        i = i + 1
        x = str(R.extract(6, i))
    i = i - 1
    for choice in semesterChoices:
        w['menu'].add_command(label=choice, command= lambda value=choice: semesterText.set(value))
    semesterText.trace("w", changeClass)
    #Puts current student semesters into semesterChoices list
    #Sets semester drop menu to semesterChoices
    #semesterText is traced so if semesterText changes, run changeClass 

    list1.delete(0, END)
    #Clears current listbox
    k = 1
    x = str(R.extract(7, 1, k))
    while x != "":
        list1.insert(k, str(R.extract(7, 1, k)))
        k = k + 1
        x = str(R.extract(7, 1, k))
    i = 1
    #Populates classes listbox with classes in currently selected semester

####################
# Semester Changes #
####################

def changeClass(*args):
    list1.delete(0, END)
    #Clears current listbox
    
    global i, R
    #Global variables we need
    
    x = str(R.extract(6, i))
    #Sets x equal to current semester
    
    while x != semesterText.get():
        if i < 10:
            i = i + 1
            x = str(R.extract(6, i))
        else:
            i = 1
            x = str(R.extract(6, i))
    #If current semester does not match selected semester, increments until it does
    #My code currently only supports up to 10 semesters as a quick solution to an infinite loop
            
    else:
        k = 1
        x = str(R.extract(7, i, k))
        while x != "":
            list1.insert(END, str(R.extract(7, i, k)))
            k = k + 1
            x = str(R.extract(7, i, k))
    #Inserts classes of selected semester into listbox

#############
# Add Class #
#############
def addclass():
    global i, R
    #Global variables we need
    
    c = addClassPopup()
    #Opens addClassPopup class and access its variables using c
    
    root.wait_window(c.top)
    #Waits until addClassPopup closes before continuing
    
    k = 1
    x = str(R.extract(7, i, 1))
    while x != "":
        k = k + 1
        x = str(R.extract(7, i, k))
    else:
        R.insert(7, i, k, c.value)
        R.insert(8, i, k, c.value2)
    list1.insert(END, c.value)
    #Inserts class selected with grade selected into the listbox
    #c.value is the class while c.value2 is the grade of that class


class addClassPopup(object):
    def __init__(self):
        global F2
        #Global variables we need (COURSES file)
        
        top=self.top=Toplevel()
        top.configure(background = "white")
        top.geometry("300x240")
        #Creates the popup window with set configurations
        
        self.l=Label(top,text="Select class:", fg = "blue", bg = "white", font = ("Verdana", 10))
        self.l.grid(column = 0, row = 0, pady = (10, 0))
        
        self.lb=Listbox(top, width = 20, selectmode = SINGLE, fg = "blue", bg = "white", font = ("Verdana", 10))#yscrollcommand = self.scrollbar.set, width = 32, selectmode = SINGLE, bg = "white", font = ("Verdana", 10))
        self.lb.grid(row = 1, column = 0, rowspan = 5, padx = (0, 10))
        #Creates a listbox for list of classes
        
        self.l2=Label(top,text="Select grade:", fg = "blue", bg = "white", font = ("Verdana", 10))
        self.l2.grid(row = 0, column = 1, padx = (0, 10), pady = (10, 0))
        
        self.b=Button(top,text='Add Class',command=self.cleanup, fg = "blue", bg = "white", font = ("Verdana", 10), width = 10)
        self.b.grid(row = 3, column = 1, pady = 10)
        self.b=Button(top,text='More Info',command=self.moreinfo, fg = "blue", bg = "white", font = ("Verdana", 10), width = 10)
        self.b.grid(row = 4, column = 1, pady = 10)
        #Creates the two buttons, one for adding the class, one for showing more info
        #Add Class goes to cleanup function and More Info goes to moreinfo function
        
        self.od = ("A", "B", "C" ,"D", "F")
        self.ol = StringVar()
        self.ol.set(self.od[0])
        self.o = OptionMenu(top, self.ol, *self.od)
        self.o['menu'].config(bg = "white")
        self.o.config(bg = "white", font = ("Verdana", 10), width = 6)
        self.o.grid(row = 1, column = 1, pady = 10)
        self.lst = u2py.List(1, F2)
        self.x = str(self.lst.next())
        #Creates a dropdown menu with the options A, B, C, D, and F

        try:
            while self.x != "":
                self.lb.insert(END, self.x)
                self.x = str(self.lst.next())
        except u2py.U2Error:
            return
        #Populates the listbox with classes from the COURSES file
        #Once the next function reaches the end, return
        
    def cleanup(self):
        self.value=self.lb.get(ACTIVE)
        self.value2=self.ol.get()
        #Sets value to currently selected class and value2 to selected grade

        self.top.destroy()
        #Destroy popup window
        
    def moreinfo(self):
        mi = self.mi = Toplevel()
        self.mi.title(self.lb.get(ACTIVE))
        self.mi.config(background= "white")
        self.mi.geometry("280x150")
        #Creates a small popup window
        
        self.R = F2.read(self.lb.get(ACTIVE))
        #Access the COURSES file and find the information for currently selected class (in listbox)
        
        self.mil1 = Label(mi, text = "Class Number", fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 0, column = 0, pady = (20, 5), padx = 10, sticky = W)
        self.mil1 = Label(mi, text = "Class Name", fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 1, column = 0, pady = 5, padx = 10, sticky = W)
        self.mil1 = Label(mi, text = "Teacher", fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 2, column = 0, pady = 5, padx = 10, sticky = W)
        self.mil1 = Label(mi, text = "Credits", fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 3, column = 0, pady = 5, padx = 10, sticky = W)

        self.mil1 = Label(self.mi, text = self.lb.get(ACTIVE), fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 0, column = 1, pady = (20, 5), padx = 10, sticky = W)
        self.mil1 = Label(self.mi, text = str(self.R.extract(1)), fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 1, column = 1, pady = 5, padx = 10, sticky = W)
        self.mil1 = Label(self.mi, text = str(self.R.extract(3)), fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 2, column = 1, pady = 5, padx = 10, sticky = W)
        self.mil1 = Label(self.mi, text = str(self.R.extract(2)), fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 3, column = 1, pady = 5, padx = 10, sticky = W)
        #Labels for displaying the various information

################
# Remove Class #
################
def removeclass():
    global i, R
    #Global Variables we need
    
    findClass = list1.get(ACTIVE)
    #Sets findClass to currently selected class
    
    k = 1
    x = str(R.extract(7, i, k))
    while x != findClass:
        k = k + 1
        x = str(R.extract(7, i, k))
    else:
        R.delete(7, i, k)
        R.delete(8, i, k)
    #Loops through students's classes until the selected class is found
    #Removes the class and its respective grade from the Dynamic Array
        
    items = list1.curselection()
    pos = 0
    for j in items:
        idx = int(j) - pos
        list1.delete( idx,idx )
        pos = pos + 1
    #Deletes current selection from the listbox

################
# Change Grade #
################
def changegrade():
    global i, R
    #Global variable we need

    g = addGradePopup()
    #Opens addClassPopup class and access its variables using g

    root.wait_window(g.top)
    #Waits until addGradePopup closes before continuing
    
    findGrade = list1.get(ACTIVE)
    #Sets findGrade to currently selected class
    
    k = 1
    x = str(R.extract(7, i, k))
    while x != findGrade:
        k = k + 1
        x = str(R.extract(7, i, k))
    else:
        R.replace(8, i, k, g.value)
class addGradePopup(object):
    def __init__(self):
        top=self.top=Toplevel()
        top.configure(background = "white")
        top.geometry("130x160")
        #Creates popup window
        
        self.l=Label(top,text="New Grade:", fg = "blue", bg = "white", font = ("Verdana", 10))
        self.l.grid(row = 0, column = 0, pady = (10, 0))

        self.b=Button(top,text='Change Grade',command=self.cleanup, fg = "blue", bg = "white", font = ("Verdana", 10), width = 12)
        self.b.grid( row = 2, column = 0, pady = 10)
        #Creates button that runs cleanup function
        
        self.od = ("A", "B", "C" ,"D", "F")
        self.ol = StringVar()
        self.ol.set(self.od[0])
        self.o = OptionMenu(top, self.ol, *self.od)
        self.o['menu'].config(bg = "white") 
        self.o.config(bg = "white", font = ("Verdana", 10), width = 8)
        self.o.grid(row = 1, column = 0, pady = 10)
        #Creates a dropdown menu that has the options A, B, C, D, and F
        
    def cleanup(self):
        self.value=self.ol.get()
        #Sets value to currently selected grade in the dropdown menu
        
        self.top.destroy()
        #Destroys popup window

################
# Save Changes #
################
def savechanges():
    
    R.replace(1, lnameText.get())
    R.replace(2, fnameText.get())
    R.replace(3, majorText.get())
    R.replace(4, minorText.get())
    R.replace(5, advisorText.get())
    #Replaces Dynamic Array content with ones in the entry
    
    F.write(entryText.get(), R)
    #Overwrites the current student's entry in the STUDENT file with the Dynamic Array
    
    messageWindow()
    #Popupwindow confirming changes

def messageWindow():
    win = Toplevel()
    win.title('Save Successful')
    win.config(background= "white")
    win.geometry("240x100")
    message = "Your file was successfully saved."
    Label(win, text=message, bg = "white", fg = "blue", font = ("Verdana", 10)).pack(pady = 10)
    Button(win, text='Ok', command=win.destroy, bg = "white", fg = "blue", font = ("Verdana", 10), width = 10).pack(pady = 10)

###############
# Report Card #
###############
def reportcard():
    global R, F, F2
    #Global variables we need

    TC = u2py.DynArray("COURSE_NBR")
    TC.insert(2, "TEACHER")
    #TC is a Dynamic Array that refers to the COURSE_NBR and TEACHER virtual fields in STUDENT
    
    D = F.readnamedfields(entryText.get(), TC)
    #D accesses the COURSE_NBR and TEACHER for the current student
    
    G = u2py.DynArray("GPA1")
    result = F.readnamedfields(entryText.get(), G)
    #Similar to the previous lines, G refers to the virtual GPA1 field in STUDENTS

    rc = Toplevel()
    rc.title('Report Card for ' + str(R.extract(2)) + " " + str(R.extract(1)))
    rc.config(background= "white")
    rc.geometry("500x800")
    rc.columnconfigure(0, minsize = 80)
    rc.columnconfigure(1, minsize = 80)
    rc.columnconfigure(2, minsize = 60)
    rc.columnconfigure(3, minsize = 60)
    rc.columnconfigure(4, minsize = 80)
    #Creates popup menu
    
    rcl1 = Label(rc, text = "First Name", fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 0, column = 0, pady = 10, sticky = W)
    rcl1 = Label(rc, text = "Last Name", fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 0, column = 1, pady = 10, sticky = W)
    rcl1 = Label(rc, text = "Major", fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 0, column = 2, pady = 10, sticky = W)
    rcl1 = Label(rc, text = "Minor", fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 0, column = 3, pady = 10, sticky = W)
    rcl1 = Label(rc, text = "Advisor", fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 0, column = 4, pady = 10, sticky = W)
    rcl1 = Label(rc, text = "GPA", fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 0, column = 5, pady = 10, sticky = W)
    rcl1 = Label(rc, text = result, fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 2, column = 5, pady = (0, 10), sticky = W)

    rcl1 = Label(rc, text = str(R.extract(2)), fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 2, column = 0, pady = (0, 10), sticky = W)
    rcl1 = Label(rc, text = str(R.extract(1)), fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 2, column = 1, pady = (0, 10), sticky = W)
    rcl1 = Label(rc, text = str(R.extract(3)), fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 2, column = 2, pady = (0, 10), sticky = W)
    rcl1 = Label(rc, text = str(R.extract(4)), fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 2, column = 3, pady = (0, 10), sticky = W)
    rcl1 = Label(rc, text = str(R.extract(5)), fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 2, column = 4, pady = (0, 10), sticky = W)

    rcl1 = Label(rc, text = "Semester", fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 4, column = 0, pady = (20, 10), sticky = W)
    rcl1 = Label(rc, text = "Classes", fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 4, column = 1, pady = (20, 10), sticky = W)
    rcl1 = Label(rc, text = "Grade", fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 4, column = 6, pady = (20, 10), sticky = W)
    rcl1 = Label(rc, text = "Teacher", fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 4, column = 4, pady = (20, 10), sticky = W)
    rcl1 = Label(rc, text = "Credits", fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 4, column = 5, pady = (20, 10), sticky = W)
    #Various labels to display student information

    #THE FOLLOWING CODE ONLY DISPLAYS 2 SEMESTERS OF CLASSES
    #You can make a loop to display more semesters
    i = 1
    k = 1
    y = str(R.extract(7, i, k))
    z = str(R.extract(8, i, k))
    f2= str(D.extract(2, 1, i))
    x = str(R.extract(6, i))
    rcl1 = Label(rc, text = x, fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 4 + i, column =0, pady = 5, sticky = W)
    C = F2.read(y)
    #Various variables we need to update throughout the Loop
    #y is class, z is grade, f2 is teacher, x is semester
    #This code is suppose to loop through each class in a semester, then loop through the semesters
    
    while y != "":
        
        rcl1 = Label(rc, text = str(C.extract(1)), fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 4 + k, column =1, columnspan = 5, pady = 5, sticky = W)
        rcl1 = Label(rc, text = z, fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 4 + k, column =6, pady = 5, sticky = W)
        rcl1 = Label(rc, text = str(C.extract(2)), fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 4 + k, column =5, pady = 5, sticky = W)
        rcl1 = Label(rc, text = f2, fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 4 + k, column =4, pady = 5, sticky = W)

        k = k + 1
        y = str(R.extract(7, i, k))
        z = str(R.extract(8, i, k))
        f2= str(D.extract(2, 1, k))
        if y !="":
            C = F2.read(y)
    else:
        i = i + 1
        x = str(R.extract(6, i))
        rcl1 = Label(rc, text = x, fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = 5 + k, column =0, pady = 5, sticky = W)
        k2 = k + 4
    #Displays the classes and its information in the first semester and increments the semester
        
    k = 1
    y = str(R.extract(7, i, k))
    z = str(R.extract(8, i, k))
    f2= str(D.extract(2, 2, k))
    C = F2.read(y)
    #Sets variables to the first class in the second semester
    
    while y != "":
        rcl1 = Label(rc, text = str(C.extract(1)), fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = k2 + k, column =1, columnspan = 5, pady = 5, sticky = W)
        rcl1 = Label(rc, text = z, fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = k2 + k, column =6, pady = 5, sticky = W)
        rcl1 = Label(rc, text = str(C.extract(2)), fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = k2 + k, column =5, pady = 5, sticky = W)
        rcl1 = Label(rc, text = f2, fg = "blue", bg = "white", font = ("Verdana", 8)).grid(row = k2 + k, column =4, pady = 5, sticky = W)

        k = k + 1
        y = str(R.extract(7, i, k))
        z = str(R.extract(8, i, k))
        f2= str(D.extract(2, 2, k))
        if y != "":
            C = F2.read(y)
    #Displays the classes and its information in the second semester

########
# Quit #
########
def quittest():
    root.destroy()
    #Exits the GUI window

#canvas
canvas1 = Canvas(root, height = 100, bg = "blue", width = 800).grid(row = 0, column = 0, columnspan = 10)
image1 = PhotoImage(file = "logo.gif")
image2 = Label(root, image = image1, height=100).grid(row = 0,column=0, columnspan = 10, sticky = W)
#An optional step to create the Rocket Logo and the blue background
#Only GIF images are accepted

#menu
menubar = Menu(root, tearoff= 0)
menu1 = Menu(menubar)
menu1.add_command(label = "Quit", command = quittest)
menubar.add_cascade(label = "File", menu = menu1)
root.config(menu = menubar)
#This is how you create the menu bar in TKinter
#The only relevant option was Quit for me but you can add anything other function you want

#buttons
label1 = Label(text = "Search Student ID", fg = "blue", bg = "white", font = "Verdana").grid(row = 5, column = 0, pady = (20,10), columnspan = 2, sticky = W)
entry1 = Entry(root, textvariable = entryText, font = "Verdana", width = 12).grid(row = 5, column = 2, pady = (20,10), sticky = W)
button1 = Button(root, text = "Search", command = search, fg = "blue", bg = "white", font = ("Verdana", 10), width = 14).grid(row = 5, column = 3, pady = (20,10), sticky = W)
button5 = Button(root, text = "Add Class", command = addclass, fg = "blue", bg = "white", font = ("Verdana", 10), width = 14).grid(row = 21, column = 2, pady = (10, 10), sticky = W)
button6 = Button(root, text = "Remove Class", command = removeclass, fg = "blue", bg = "white", font = ("Verdana", 10), width = 14).grid(row = 22, column = 2, pady = 15, sticky = W)
button7 = Button(root, text = "Save Changes", command = savechanges, fg = "blue", bg = "white", font = ("Verdana", 10), width = 14).grid(row = 21, column = 3, pady = 15, sticky = W)
button8 = Button(root, text = "Quit", command = quittest, fg = "blue", bg = "white", font = ("Verdana", 10), width = 14).grid(row = 23, column = 3, pady = 15, sticky = W)
button9 = Button(root, text = "Change Grade", command = changegrade, fg = "blue", bg = "white", font = ("Verdana", 10), width = 14).grid(row = 23, column = 2, pady = 15, sticky = W)
button10 = Button(root, text = "Report Card", command = reportcard, fg = "blue", bg = "white", font = ("Verdana", 10), width = 14).grid(row = 22, column = 3, pady = (10, 10), sticky = W)
#These are the buttons that call their relative funtions

#modify
label4 = Label(text = "First Name:", fg = "blue", bg = "white", font = ("Verdana", 10)).grid(row = 10, column = 0, pady = 10, sticky = W)
data_fname = Entry(root, textvariable = fnameText, bg = "white", font = ("Verdana", 10), width = 15).grid(row = 10, column = 1, pady = 1, sticky = W)
label5 = Label(text = "Last Name:", fg = "blue", bg = "white", font = ("Verdana", 10)).grid(row = 10, column = 2, pady = 10, sticky = W)
data_lname = Entry(root, textvariable = lnameText, bg = "white", font = ("Verdana", 10), width = 15).grid(row = 10, column = 3,  pady = 10, sticky = W)
label6 = Label(text = "Major:", fg = "blue", bg = "white", font = ("Verdana", 10)).grid(row = 11, column = 0, pady = 10, sticky = W)
data_major = Entry(root, textvariable = majorText, bg = "white", font = ("Verdana", 10), width = 15).grid(row = 11, column = 1, pady = 10, sticky = W)
label7 = Label(text = "Minor:", fg = "blue", bg = "white", font = ("Verdana", 10)).grid(row = 11, column = 2, pady = 10, sticky = W)
data_minor = Entry(root, textvariable = minorText, bg = "white", font = ("Verdana", 10), width = 15).grid(row = 11, column = 3, pady = 10, sticky = W)
label8 = Label(text = "Advisor:", fg = "blue", bg = "white", font = ("Verdana", 10)).grid(row = 12, column = 2, pady = 10, sticky = W)
data_advisor = Entry(root, textvariable = advisorText, bg = "white", font = ("Verdana", 10), width = 15).grid(row = 12, column = 3, pady = 10, sticky = W)
label3 = Label(text = "Semester:", fg = "blue", bg = "white", font = ("Verdana", 10)).grid(row = 12, column = 0, sticky = W)
#Labels are just blocks of text
#These can all be changed through functions and such

#optionmenu
semesterChoices = [""]
w = OptionMenu(root, semesterText, *semesterChoices)
w['menu'].config(bg = "white")
w.config(bg = "white", font = ("Verdana", 10), width = 10)
w.grid(row = 12, column = 1, sticky = W)
#This created the dropdown menu for selecting the different semesters available

list1 = Listbox(root, width = 32, selectmode = SINGLE, bg = "white", font = ("Verdana", 10))
list1.grid(row = 21, column = 0, rowspan = 10, pady = (10,0), columnspan = 2, sticky = W)
#This created the listbox for the classes that are displayed for a semester

root.mainloop()





















