import time
global jsonfile
jsonfile = "data.json"
import random
import json
global sensor
sensor = 10
print("Before starting:")                       #||
print("which 'sensor' should be tested?")       #||
print("valid sensors: 0  and  1")               #||
while sensor == 10:                             #||
    sensor = int(input())                       #||
    if sensor != 0:                             #|| STARTUP
        if sensor != 1:                         #|| Sets sensor to 1 or 0
            print("ERROR INVALID SENSOR INPUT") #||
            sensor = 10                         #||
print("Proceeding...")                          #||
print("What should be tested?")                 #||
p = 0                                           #||

while p <= 10:
    if sensor == 0:
        jsonfile = "data.json"
    else:
        jsonfile = "data2.json"

    key = input()
    if key == "encode":                             ##################### ENCODING #####################
        #complete
        ################################################################################    ENCODING START


        def data0(level, value):
            with open(jsonfile, 'r+') as f:
                global data
                data = json.load(f)
                data[level] = value # <--- data[ref] = measurements.
                f.seek(0)        # <--- resets file position to the beginning.
                json.dump(data, f, indent=4)
                f.truncate()     # remove remaining part


        ################################################################################    ENCODING FINISH
        
        def trigger0():
            global triggav0
            triggav0 = 0                                                 #||
            for i in range(10):                                          #||
                global trigg0
                trigg0 = random.uniform(0.5, 5)                             #||  Data collection
                print(trigg0)
                                                          #||
                triggav0 = triggav0 + trigg0
                #triggav0 = int(trigg0) / 10   # Average                   ||
                time.sleep(.2) # Actual delay in data transmission. Any faster seems to give exponential delays to data over time in real code.
        
        #########################################################################
        lev = 0                           #||                                   |S
        for q in range(19):               #||                                   |T
            print(lev,':')                #||                                   |O
            trigger0()                    #|| Data storage                      |R
            triggav0 = int(triggav0) / 10
            data0(lev, triggav0) # implementing vars to function                |A
            print(triggav0)               #||                                   |G
            lev = lev+1                   #||                                   |E

        #########################################################################
        data0('end', 'value') # Prevents duplicate values   |Completion
        print('Complete') #                                 |
        #####################################################

    else:
        if key == "decode":                             ##################### DECODE #####################
            print("DECODE ACTIVATED")
            time.sleep(1)
            av0 = 0
            import length
            from length import file_length
            for ref in range(file_length):
                import json_reader
                json_reader.readfile()
                print(ref,':', json_reader.val)

        else:
            if key == "calibrate":                             ##################### CALIBRATE #####################
                print("calibration starting")
                time.sleep(1)
                #####################
                global relav0     #||:::::::::::::::::::::::::::
                global error0     #|| |||||||||||||||||||||||||
                relav0 = .5       #||  Not included in main.py
                error0 = .5       #|| |||||||||||||||||||||||||
                sens0 = 0         #||:::::::::::::::::::::::::::
                #####################
                def calibrate(sensor, file, av, error):
                    def validity_check0(variable):                                #||
                        global valid0                                             #||
                        if float(variable) <= float(av) + float(error) + .5:      #|| <--- Used to contain relav0 and error0
                            print(f"{variable} INVALID")                          #||
                            print(f"terminating {variable}")                      #|| Validity check sens0
                            valid0 = 1                                            #||
                        else:                                                     #||
                            print("triggav0 VALID")                               #||
                            valid0 = 0                                            #||
                    #================================================================
                    largestval0 = 0
                    global ref
                    av0 = 0                                       #||
                    import length                  #|             #||
                    from length import file_length #|             #||
                    for ref in range(file_length): #| Reading     #||
                        import json_reader         #|             #|| Data verification and averaging
                        json_reader.readfile()     #|             #||
                        validity_check0(json_reader.val)          #||
                        if valid0 == 0:                           #||
                            av0 = av0 + json_reader.val           #||
                            if json_reader.val >= largestval0:     #| sets data range
                                largestval0 = json_reader.val      #| sets data range
                        else:
                            jsonfile = 'invalid.json'  # Currently has no function
                            print(ref, 'invalid')
                    av0 = av0 / file_length
                    #++++++++++++++++++++++++++++++++++++++++
                jsonfile = "data.json"
                av0 = .5
                calibrate(sensor, "data.json", av0, error0)
                print("=======================================================")
                print("=======================================================")
                print("=======================================================")
                print("starting with next file")
                time.sleep(1)
                jsonfile = "data2.json"
                av0 = .5
                calibrate(sensor, "data.json", av0, error0)
            
            else:
                if key == "change sensor":
                    maybesens = int(input())
                    if maybesens == 1:
                        sensor = maybesens
                    else:
                        if maybesens == 0:
                            sensor = maybesens
                        else:
                            print("INVALID INPUT")
                
                else:
                    if key == "reply test":
                        print("hi")
    