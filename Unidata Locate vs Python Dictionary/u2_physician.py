#!/bin/python3
#Program: u2_physician.py
#Purpose: Compare UDT Locate vs Python Dictionary

import sys
import u2py
import time

start = time.time(); 

try:
    u2file=u2py.File("PHYSICIAN")
    mcmd = u2py.Command("SELECT PHYSICIAN")
    mcmd.run()
    U2List=u2py.List(0)
except Exception as e:
    print(str(e))

KEY={};
for id in U2List:
    rec=u2file.read(id)
    gender=rec.extract(8,0,0)
    specialty=rec.extract(12,0,0)
    year=rec.extract(11,0,0)
    school=rec.extract(10,0,0)
    city=rec.extract(25,0,0)
    state=rec.extract(26,0,0)
    key=str(state)
    if key in KEY:
        KEY[key] +=1
    else:
        KEY[key] = 1

U2List.clear()

RevSort=[]
for k in KEY.keys():
    v=KEY[k]
    RevSort.append((v,k)) #trick to sort.

RevSort.sort(reverse=True)

for (v,k) in RevSort[:10]:
    print ("%s => %s" % (k,v  ) )

print("# of Categories:",len(RevSort))
print("Time:",(time.time() - start))

sys.exit()
