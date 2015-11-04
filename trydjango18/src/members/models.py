from django.db import models


def readmember(formdata, uvfields, formfields):
    # get the UniVerse imports
    import os
    os.chdir("C:\\U2\\XDEMO\\pythonbetarocket")
    import u2py

    member_id = formdata.get('member_id')
    # read the file and get the details
    file = u2py.File("MEMBERS")
    field_names = u2py.DynArray()
    for pos, dictname in uvfields.items():
        field_names.replace(pos, dictname)
    member_data = file.readnamedfields(member_id, field_names)
    formdata['member_id'] = member_id
    for pos, dictname in formfields.items():
        formdata[dictname] = member_data.extract(pos)
    return formdata


def writemember(formdata, uvfields, formfields):
    # get the UniVerse imports
    import os
    os.chdir("C:\\U2\\XDEMO\\pythonbetarocket")
    import u2py

    # open the file, read the latest version and write the details away
    file = u2py.File("MEMBERS")
    member_id = formdata.get('member_id')
    field_names = u2py.DynArray()
    for pos, dictname in uvfields.items():
        field_names.replace(pos, dictname)
    member_data = u2py.DynArray()
    if member_id == "NEW":
        # need to generate a new key
        member_id = genuniquekey("MEMBERS", 4)
    for pos, dictname in formfields.items():
        member_data.replace(pos, formdata.get(dictname))
    file.writenamedfields(member_id, field_names, member_data)
    # set the return key
    formdata['member_id'] = member_id


def searchmember(formdata, uvfields, formfields):
    # get the UniVerse imports
    import os
    os.chdir("C:\\U2\\XDEMO\\pythonbetarocket")
    import u2py

    thecmd = "SELECT MEMBERS WITH"
    loopcntr = 0
    # loop through the fields and build the select list
    for pos, dictname in formfields.items():
        if formdata[dictname] != "":
            loopcntr += 1
            if loopcntr > 1:
                thecmd += " OR"
            thecmd += ' ' + str(uvfields.get(pos)) + ' = "' + str(formdata.get(dictname)) + '"'
    command = u2py.Command("CLEARSELECT")
    command = u2py.Command(thecmd)
    command.run()
    rtnlist = []
    print(thecmd)
    try:
        thelist = u2py.List(0)
        thedynlist = thelist.readlist()
        print(str(thedynlist))
    except u2py.U2Error as e:
        return rtnlist





def genuniquekey(filename, mask):
    # get the UniVerse imports
    import os
    os.chdir("C:\\U2\\XDEMO\\pythonbetarocket")
    import u2py

    sub = u2py.Subroutine("GEN.UNIQUE.KEY", 5)
    sub.args[0] = filename
    sub.args[1] = mask
    sub.call()
    if str(sub.args[3]) != "0":
        print("Error!!!! " + str(sub.args[4]))
    else:
        newkey = str(sub.args[2])
        return newkey


# Create your models here.
class Members(models.Model):
    id = models.CharField(max_length=10, blank=False, null=False, primary_key=True)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField()

    def __str__(self):
        return self.id
