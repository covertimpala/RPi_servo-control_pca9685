import time
jsonfile = "data.txt"
import random
import json
print(".")

#complete
################################################################################    ENCODING START


def data0(level, value):
    with open('data.json', 'r+') as f:
        global data
        data = json.load(f)
        data[level] = value # <--- data[ref] = measurements.
        f.seek(0)        # <--- resets file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()     # remove remaining part


################################################################################    ENCODING FINISH
#already in place
def trigger0():                                                  #||
    for i in range(10):                                          #||
        trigg0 = random.randrange(0,5)                           #||  Data collection
        global triggav0                                          #||
        triggav0 = int(trigg0) / 11   # Average                   ||

#########################################################################
lev = 1                           #||                                   |S
for q in range(19):               #||                                   |T
    print(lev,':')                #||                                   |O
    trigger0()                    #|| Data storage                      |R
    data0(lev, triggav0) # implementing vars to function                |A
    print(triggav0)               #||                                   |G
    lev = lev+1                   #||                                   |E
    time.sleep(1)                 #||                                   |!
#########################################################################
data0('end', 'value') # Prevents duplicate values   |Completion
print('Complete') #                                 |
#####################################################