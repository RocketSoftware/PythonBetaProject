This is a readme for the Python GUI demo application for running 
UniData commands. To run this application, you must have UniData 
8.1(or 2) installed with the STUDENT and COURSES file in the demo folder.

Copy all the files to the C:\U2\ud81\python directory.  Move the Python Demo shortcut to the desktop and the logo.gif to the C:\U2\ud81\demo directory.  



Use the shortcut or Open a command prompt and navigate to the C:\U2\ud81\demo folder. Once you are in the demo folder, enter "python PythonStudentDemov1.0.0.py".  Make sure that C:\U2\ud81\python is in the default search path (PATH=%PATH%;C:\U2\ud81\python)



Unidata 8.1 includes a package named u2py that reads UniData 
commands from Python. In the Search Student ID entry box, enter the 
student ID of the student whose information you want to edit.The 
search button uses the u2py read command to extract the student’s 
information from the STUDENT file as a dynamic array. Once the 
search button is clicked, the application will use the u2py extract 
function to send the information to each entry box. Each of these 
entry boxes you see can be edited. The student's classes are 
displayed in the list box on the bottom right. By default, the 
student's earliest semester is selected. Use the dropdown menu to 
select the semester you want to modify. Once the desired semester is 
selected, use the Add Class button to open a popup. This new window 
will have a list of all the classes located in the COURSES file. To 
see more information about a specific class, click the More Info 
button to open a new window displaying the course abbreviation, 
course name, teacher name, and credit hours. Once a class is selected, 
select a matching grade for the class. Once the Add Class button is 
added, the class will be added to the list box as well as in the 
dynamic array along with its grade. To remove a class, selected the 
class from the list box and click the Remove Class button. This will 
remove the class and its grade from the dynamic array and remove it 
from the list box as well. To change the grade of a class that the 
student is already assigned, click the Change Grade button. This opens 
a popup with a dropdown menu to select a grade. The selected grade 
will replace the current grade for that class when the Change Grade 
button is clicked. No changes will be made to the STUDENT file until 
the Save Changes button is clicked. This replaces the student entry in 
the file with the student’s information in our dynamic array. Once 
clicked, a confirmation window will popup confirming these changes. The 
Report Card button reads the STUDENT file for the current student and 
displays all the information available. This is a good way of checking 
the student’s information is changed and correct. Finally, the Quit 
button will exit the GUI application when you are finished. 
