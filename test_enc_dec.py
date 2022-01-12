import time
jsonfile = "data.txt"
import random
import json
print("What should be tested?")
p = 0

while p <= 10:
    key = input()
    if key == "encode":
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
    
        def trigger0():                                                  #||
            for i in range(10):                                          #||
                trigg0 = random.randrange(0,5)                           #||  Data collection
                global triggav0                                          #||
                triggav0 = int(trigg0) / 11   # Average                   ||

        #########################################################################
        lev = 0                           #||                                   |S
        for q in range(19):               #||                                   |T
            print(lev,':')                #||                                   |O
            trigger0()                    #|| Data storage                      |R
            data0(lev, triggav0) # implementing vars to function                |A
            print(triggav0)               #||                                   |G
            lev = lev+1                   #||                                   |E

        #########################################################################
        data0('end', 'value') # Prevents duplicate values   |Completion
        print('Complete') #                                 |
        #####################################################

    else:
        if key == "read" or "decode":
            av0 = 0
            import length
            from length import file_length
            for ref in range(file_length):
                import json_reader
                json_reader.readfile()
                print(ref,':', json_reader.val)

        else:
            if key == "data calibration":
                #####################
                global relav0     #||:::::::::::::::::::::::::::
                global error0     #|| |||||||||||||||||||||||||
                relav0 = .5       #||  Not included in main.py
                error0 = .5       #|| |||||||||||||||||||||||||
                sens0 = 0         #||:::::::::::::::::::::::::::
                #####################
                def calibrate(sensor, triggav, file, av, error):
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
                    av0 = 0                                       #||
                    import length                                 #||
                    from length import file_length                #||
                    for ref in range(file_length):                #||
                        import json_reader                        #|| Data verification and averaging
                        json_reader.readfile()                    #||
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

                calibrate(sens0, triggav0, "data.txt", av0, error0)