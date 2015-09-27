This is a readme for the Python GUI MembersDemo sample application (version 1.1.0) to work with u2py module. 

To run this application, you must have UniData 8.2 or UniVerse 11.3.1 installed with 
the MEMBERS and STATES file in the XDEMO account.

Copy the MembersDemo.py file to the XDEMO or XDEMO\PP directory. If the MembersDemo.py program 
is not running from default XDEMO location (e.g. c:\temp\XDEMO), you will need to update the u2bin parameter in the 
MembersDemo.cfg configuration file.

Use the shortcut or Open a command prompt and navigate to the C:\U2\ud82\XDEMO or C:\U2\UV\XDEMO folder. 
Once you are in the XDEMO or XDEMO\PP folder, enter "python Members.py".  Make sure that C:\U2\ud82\python 
or C:\U2\UV\python is in the default search path (PATH=C:\U2\ud82\python;%PATH% or PATH=C:\U2\UV\python;%PATH%)

Unidata 8.2.0 or UniVerse 11.3.1 includes a package named u2py that reads U2 commands from Python. 

This sample program demonstrates the following functions:

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

Sample MembersDemo.cfg file:

[appSettings]
id = 0133
u2bin = c:\U2\ud82\bin
account_path = c:\U2\ud82\XDEMO