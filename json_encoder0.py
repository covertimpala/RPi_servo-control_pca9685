import json
from __main__ import lev, triggav0

lev = 9
triggav0 = 79

def data0(level, value):
    with open('data.json', 'r+') as f:
        global data
        data = json.load(f)
        data[level] = value # <--- add `id` value.
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()     # remove remaining part
        

data0(lev, triggav0) # implementing vars from __main__ into function
print(lev)

with open('data.json', 'r+') as f:          #||
    global data                             #||
    data = json.load(f)                     #||
    data['end'] = 'value'                   #|| Indicates end in file and avoids software from making duplicates
    f.seek(0)                               #||
    json.dump(data, f, indent=4)            #||
    f.truncate()                            #||