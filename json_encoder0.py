print("starting")
import json
from __main__ import lev, triggav0, jsonfile   #| imports variables from main file



#lev = 9          #|For testing and troubleshooting
#triggav0 = 79    #|For testing and troubleshooting

print(lev)
print(triggav0)

def data0(level, value):
    with open('data.json', 'r+') as f:
        global data
        data = json.load(f)
        data[level] = value # <--- data[ref] = measurements.
        f.seek(0)        # <--- resets file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()     # remove remaining part
        

data0(lev, triggav0) # implementing vars from __main__ into function
print(lev)
data0('end', 'value') # Prevents duplicate values