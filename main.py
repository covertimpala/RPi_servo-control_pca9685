import time
import json
import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
from adafruit_servokit import ServoKit
from multiprocessing import Pool
import RPi.GPIO as GPIO

import adafruit_motor.servo
import serial


GPIO . setmode ( GPIO . BCM )
GPIO . setup ( 18 , GPIO . OUT )
# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)
kit.servo.frequency = 50
kit.servo[0].actuation_range = 180
kit.servo[1].actuation_range = 120
kit.servo[2].actuation_range = 130
kit.servo[3].actuation_range = 90  #still needs adjustment
kit.servo[4].actuation_range = 180  #still needs adjustment
kit.servo[5].actuation_range = 180   #range 90 = open 132 = closed
run = 0
lock = 0
speed = 0
EMG = 0
while run <= 100:
    key = input()
    if key == "0":
        print("choose angle")
        angle = int(input())
        kit.servo[0].angle = angle
        

    else:
        if key == "1":
            print("choose angle")
            angle = int(input())
            
            if lock == 1:
                change_angle = int(angle) - int(round(int(kit.servo[1].angle)))
                kit.servo[1].angle = angle
                if int(round(int(kit.servo[2].angle) + int(change_angle))) >= 0:
                    kit.servo[2].angle = int(round(int(kit.servo[2].angle) + int(change_angle)))
                    print(int(change_angle))
                    print(round(kit.servo[2].angle + change_angle))
                else:
                    kit.servo[2].angle = 0
                    print("cant engage lock")
            else:
                if lock == 2:
                    change_angle = int(angle) - int(round(int(kit.servo[1].angle)))
                    kit.servo[1].angle = angle
                    if int(round(int(kit.servo[3].angle) + int(change_angle))) >= 30:
                        kit.servo[3].angle = int(round(int(kit.servo[3].angle) + int(change_angle)))
                    else:
                        kit.servo[3].angle = 30
                        print("cant engage lock")

                else:
                    kit.servo[1].angle = angle

        else:
            if key == "exit":
                print("exiting")
                exit()

            else:
                if key == "idle":
                    print("going to idle pos")
                    kit.servo[1].angle = 20
                    time.sleep(2)
                    kit.servo[2].angle = 7
                    time.sleep(2)
                    kit.servo[3].angle = 25
                    time.sleep(2)
                    kit.servo[0].angle = 180
                    time.sleep(2)
                    kit.servo[4].angle = 140
                    time.sleep(2)
                    kit.servo[5].angle = 130
                    print("arm has been returned to idle pos")

                else:
                    if key == "2":
                        print("choose angle")
                        angle = int(input())
                        
                        if lock == 2:
                            change_angle = int(angle) - int(round(int(kit.servo[2].angle))) * -1
                            kit.servo[2].angle = angle
                            if int(round(int(kit.servo[3].angle) + int(change_angle))) >= 30:
                                kit.servo[3].angle = int(round(int(kit.servo[3].angle) + int(change_angle)))
                            else:
                                kit.servo[3].angle = 30
                                print("cant engage lock")
                        else:
                            kit.servo[2].angle = angle
                                
                            

                    else:
                        if key == "3":
                            print("choose angle")
                            angle = int(input())
                            kit.servo[3].angle = angle

                        else:
                            if key == "4":
                                print("choose angle")
                                angle = int(input())
                                kit.servo[4].angle = angle

                            else:
                                if key == "5":
                                    print("choose angle")
                                    angle = int(input())
                                    kit.servo[5].angle = angle

                                else:
                                    if key == "test":
                                        import testsubprocess
                                        import testsub2

                                    else:
                                        if key == "angle":
                                            print("insert servo num")
                                            servo_val = int(input())
                                            servo_angle = kit.servo[servo_val].angle
                                            print(f"servo {servo_val} angle ≈ {round(servo_angle)}")

                                        else:
                                            if key == "range":
                                                print("")
                                                print("================================================")
                                                print("=========== angle ranges for servos ============")
                                                print("================================================")
                                                print("")
                                                print(f"servo [0] = {kit.servo[0].actuation_range}")
                                                print(f"servo [1] = {kit.servo[1].actuation_range}")
                                                print(f"servo [2] = {kit.servo[2].actuation_range}")
                                                print(f"servo [3] = {kit.servo[3].actuation_range}")
                                                print(f"servo [4] = {kit.servo[4].actuation_range}")
                                                print(f"servo [5] = {kit.servo[5].actuation_range}")

                                            else:
                                                if key == "help":
                                                    print("")
                                                    print("---------------------------------------------------")
                                                    print("- - - - - - - - - C O M M A N D S - - - - - - - - -")
                                                    print("---------------------------------------------------")
                                                    print("")
                                                    print("Move servo:")
                                                    print("<Servo_num>")
                                                    print("<Angle>")
                                                    print("")
                                                    print("Return to idle pos:")
                                                    print("idle")
                                                    print("")
                                                    print("Get angle ranges for servos:")
                                                    print("range")
                                                    print("")
                                                    print("leave the program:")
                                                    print("exit")
                                                    print("")
                                                    print("lock servo angle:")
                                                    print("lock")
                                                    print("to unlock:")
                                                    print("unlock")
                                                    print("")
                                                    print("activate/deactivate EMG sensors:")
                                                    print("emg <on/off>")
                                                    

                                                else:
                                                    if key == "speed":
                                                        print("servo:")
                                                        servo = int(input())
                                                        current_angle = round(int(kit.servo[servo].angle))
                                                        print("angle:")
                                                        angle = int(input())
                                                        print("speed:")
                                                        speed = int(input())
                                                        speed_percent = round(speed / angle * 100)
                                                        print(f"speed set to {speed_percent}")
                                                        f = current_angle
                                                        if current_angle < angle:
                                                            while f in range(0, int(angle)):
                                                                print(f)
                                                                kit.servo[servo].angle = f
                                                                f = int(f + int(speed_percent))

                                                        else:
                                                            print("e")
                                                            while f in range(int(angle), 180):
                                                                print(f)
                                                                kit.servo[servo].angle = f
                                                                f = int(f - int(speed_percent))

                                                    else:
                                                        if key == "led on":
                                                            GPIO.output(18, True)
                                                            print("led is on")

                                                        else:
                                                            if key == "led off":
                                                                GPIO.output(18, False)
                                                                print("led is off")

                                                            else:
                                                                if key == "lock":
                                                                    print("servo to lock (2 or 3)")
                                                                    servo_lock = int(input())
                                                                    if servo_lock == 2:
                                                                        lock = 1

                                                                    else:
                                                                        if servo_lock == 3:
                                                                            lock = 2

                                                                    print("sucess!!")
                                                                    

                                                                else:
                                                                    if key == "unlock":
                                                                        print("unlocking servos")
                                                                        lock = 0
                                                                        print("servo(s) unlocked")


                                                                    else:
                                                                        if key == "emg on":
                                                                            EMG = 1
                                                                            print("activating code")
                                                                            emgservo = 0
                                                                            status1 = "0"
                                                                            time.sleep(2)
                                                                            statsense = 0
                                                                            print("EMG ACTIVE")
                                                                            while EMG == 1:
                                                                                
                                                                                import serial_comm
                                                                                
                                                                                if __name__ == "__main__":
                                                                                    serial_comm.sensors()
                                                                                    ####
                                                                                    if float(serial_comm.sens1) <= float(relav1) + float(error1):
                                                                                        status1 = "IDLE"
                                                                                    else:
                                                                                        status1 = "ACTIVE"
                                                                                        ####
                                                                                    if float(serial_comm.sens0) <= float(relav0) + float(error0)+.5:
                                                                                        status0 = "IDLE"
                                                                                        statsense = 0
                                                                                    else:
                                                                                        status0 = "ACTIVE"
                                                                                        if status1 == "ACTIVE":
                                                                                            print("h")
                                                                                            if emgservo <= 4:
                                                                                                if statsense == 0:
                                                                                                    statsense = 1
                                                                                                    emgservo = emgservo + 1
                                                                                                    print(emgservo)
                                                                                            else:
                                                                                                if statsense == 0:
                                                                                                    statsense = 0
                                                                                                    emgservo = 0
                                                                                                    print(emgservo)
                                                                                    
                                                                                            

                                                                                    if float(serial_comm.sens1) <= float(relav1) + float(error1):
                                                                                        status1 = "IDLE"
                                                                                    else:
                                                                                        status1 = "ACTIVE"
                                                                                    
                                                                                    if status1 == "IDLE":
                                                                                        if int(float(serial_comm.sens0)) >= float(triggav0) + float(error0):
                                                                                            current_angle = round(int(kit.servo[emgservo].angle))
                                                                                            if kit.servo[emgservo].actuation_range >= int(current_angle + 5):
                                                                                                kit.servo[emgservo].angle = int(current_angle + 4)
                                                                                            else:
                                                                                                print("maxangle reached")

                                                                                    if status0 == "IDLE":
                                                                                        if int(float(serial_comm.sens1)) >= float(triggav1) + float(error1):
                                                                                            current_angle = round(int(kit.servo[emgservo].angle))
                                                                                            if current_angle >= 6:
                                                                                                kit.servo[emgservo].angle = int(current_angle - 5)
                                                                                            
                                                                                
                                                                                


                                                                        else:
                                                                            if key == "emg off":
                                                                                EMG = 0
                                                                                print("sensors deactivated")



                                                                            else:
                                                                                if key == "calibrate":
                                                                                    i = 0
                                                                                    relav0 = 0
                                                                                    relav1 = 0
                                                                                    r = 0
                                                                                    import serial_comm
                                                                                    if __name__ == "__main__":
                                                                                        serial_comm.sensors()
                                                                                        print("calibration will now begin")
                                                                                        print("relax both muscles (sensors should glow green)")
                                                                                        while r == 0:
                                                                                            import serial_comm
                                                                                            if __name__ == "__main__":
                                                                                                serial_comm.sensors()
                                                                                            if int(float(serial_comm.sens0)) <= 1.3:
                                                                                                if int(float(serial_comm.sens1)) <= 1.3:
                                                                                                    r = 1
                                                                                                    print("starting in 5 sec")
                                                                                                    time.sleep(1)
                                                                                                    print("4")
                                                                                                    time.sleep(1)
                                                                                                    print("3")
                                                                                                    time.sleep(1)
                                                                                                    print("2")
                                                                                                    time.sleep(1)
                                                                                                    print("1")
                                                                                                    time.sleep(1)
                                                                                                    print("starting")
                                                                                                    large0 = 0
                                                                                                    large1 = 0
                                                                                                    while i <= 10:             # idle calibration
                                                                                                        import serial_comm
                                                                                                        if __name__ == "__main__":
                                                                                                            serial_comm.sensors()
                                                                                                        rel0 = float(serial_comm.sens0) + float(relav0)
                                                                                                        relav0 = float(rel0)
                                                                                                        rel1 = float(serial_comm.sens1) + float(relav1)
                                                                                                        relav1 = float(rel1)
                                                                                                        i = i + 1
                                                                                                        if float(serial_comm.sens0) >= float(large0):
                                                                                                            large0 = float(serial_comm.sens0)
                                                                                                        if float(serial_comm.sens1) >= float(large1):
                                                                                                            large1 = float(serial_comm.sens1)
                                                                                                        time.sleep(.2)
                                                                                                        print((serial_comm.sens0))
                                                                                                        print(relav0)
                                                                                                    print(relav0)
                                                                                                    relav0 = int(relav0) / 11
                                                                                                    relav1 = int(relav1) / 11
                                                                                                    print(f"relax0 = {relav0}")
                                                                                                    print(f"relax1 = {relav1}")
                                                                                                    print("error range:")
                                                                                                    error0 = float(large0) - float(relav0)   # data range sensor 0
                                                                                                    error1 = float(large1) - float(relav1)   # data range sensor 1
                                                                                                    print(f"0: {error0}")
                                                                                                    print(f"1: {error1}")
                                                                                                    if float(error0) >= 1:
                                                                                                        print("CALIBRATION RESULT ERROR RANGE TOO LARGE")
                                                                                                    else:
                                                                                                        if float(error1) >= 1:
                                                                                                            print("CALIBRATION RESULT ERROR RANGE TOO LARGE")
                                                                                                        else:
                                                                                                            print("RESULTS VALID")
                                                                                                            time.sleep(2)
                                                                                                            print("==========================================================")
                                                                                                            print("Tighten one arm")
                                                                                                            while r == 1:
                                                                                                                import serial_comm
                                                                                                                if __name__ == "__main__":
                                                                                                                    serial_comm.sensors()
                                                                                                                if float(serial_comm.sens0) >= float(relav0) + float(error0) + 1:       # sensor 0
                                                                                                                    print("sensor 0 triggered")
                                                                                                                    r = 2
                                                                                                                else:
                                                                                                                    if float(serial_comm.sens1) >= float(relav0) + float(error0) + 1:   # sensor 1
                                                                                                                        print("sensor 1 triggered")
                                                                                                                        r = 3

                                                                                                            print("starting in 5 sec")
                                                                                                            time.sleep(1)
                                                                                                            print("4")
                                                                                                            time.sleep(1)
                                                                                                            print("3")
                                                                                                            time.sleep(1)
                                                                                                            print("2")
                                                                                                            time.sleep(1)
                                                                                                            print("1")
                                                                                                            time.sleep(1)
                                                                                                            print("starting")

                                                                                                            i = 0
                                                                                                            trigg0 = 0
                                                                                                            trigg1 = 1
                                                                                                            if r == 2:

                                                                                                                ########################################################################## ENCODING START


                                                                                                                def data0(level, value):
                                                                                                                    with open('data.json', 'r+') as f:
                                                                                                                        global data
                                                                                                                        data = json.load(f)
                                                                                                                        data[level] = value # <--- data[ref] = measurements
                                                                                                                        f.seek(0)        # <--- resets file position to the beginning
                                                                                                                        json.dump(data, f, indent=4)
                                                                                                                        f.truncate()
                                                                                                                
                                                                                                                
                                                                                                                ########################################################################## ENCODING END


                                                                                                                def trigger0():                                                  #||
                                                                                                                    trigg0 = 0
                                                                                                                    for i in range(10):                                          #||
                                                                                                                        import serial_comm                                       #||
                                                                                                                        if __name__ == "__main__":                               #||
                                                                                                                            serial_comm.sensors()                                #|| Data collection from sensor 0
                                                                                                                        trigg0 = float(serial_comm.sens0) + float(trigg0)        #|| ETA 2.2 sec
                                                                                                                        time.sleep(.2)                                           #||
                                                                                                                        global triggav0                                          #||
                                                                                                                        triggav0 = int(trigg0) / 11   # Average                   ||
                                                                                                            #-----------------------------------------------------------------------
                                                                                                                jsonfile = 'data.json'
                                                                                                                lev = 0                           #||
                                                                                                                for q in range(19):               #||
                                                                                                                    print(lev,':')                #||
                                                                                                                    trigger0()                    #|| Data storage
                                                                                                                    data0(lev, triggav0)          #||
                                                                                                                    print(triggav0)               #||
                                                                                                                    lev = lev+1                   #||
                                                                                                            #----------------------------------------
                                                                                                                data0('end', 'value') # Prevents duplicates  |Completion
                                                                                                                print(f"data stored in file: data.json")#    |
                                                                                                            #--------------------------------------------------------------------
                                                                                                                def validity_check0(variable):                                #||
                                                                                                                    global valid0                                             #||
                                                                                                                    if float(variable) <= float(relav0) + float(error0) + .5: #||
                                                                                                                        print(f"{variable} INVALID")                          #||
                                                                                                                        print(f"terminating {variable}")                      #|| Validity check sens0
                                                                                                                        valid0 = 1                                            #||
                                                                                                                    else:                                                     #||
                                                                                                                        print("triggav0 VALID")                               #||
                                                                                                                        valid0 = 0                                            #||
                                                                            #====================================================================================================
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
                                                                                                                if largestval0 - av0 >= float(relav0) + float(error0) + .5:
                                                                                                                    largestval0 = av0 - (float(relav0) + float(error0) + .5) # sets largest val to the most valid response
                                                                                                                




                                                                                                                
                                                                                                            else:
                                                                                                                if r == 3:
                                                                                                                    while i <= 10:
                                                                                                                        import serial_comm
                                                                                                                        if __name__ == "__main__":
                                                                                                                            serial_comm.sensors()
                                                                                                                        trigg1 = float(serial_comm.sens1) + float(trigg1)
                                                                                                                        i = i + 1
                                                                                                                        time.sleep(.2)
                                                                                                                        print(trigg1)
                                                                                                                    triggav1 = int(trigg1) / 11
                                                                                                                    print(f"triggered sensor 1 average = {triggav1}")
                                                                                                                    if float(triggav1) <= float(relav1) + float(error1):
                                                                                                                        print("RESULTS INVALID")
                                                                                                                    else:
                                                                                                                        print("RESULTS VALID")

                                                                                                            time.sleep(5)
                                                                                                            print("==========================================================")
                                                                                                            print("tighten the opposite arm now")
                                                                                                            time.sleep(2)
                                                                                                            if r == 2:
                                                                                                                while r == 2:
                                                                                                                    import serial_comm
                                                                                                                    if __name__ == "__main__":
                                                                                                                        serial_comm.sensors()
                                                                                                                    if float(serial_comm.sens1) >= float(relav1) + float(error1) + .5:       # sensor 0
                                                                                                                        print("sensor 1 triggered")
                                                                                                                        print("starting")
                                                                                                                        r = 4
                                                                                                                        i = 0
                                                                                                                        while i <= 10:
                                                                                                                            import serial_comm
                                                                                                                            if __name__ == "__main__":
                                                                                                                                serial_comm.sensors()
                                                                                                                            trigg1 = float(serial_comm.sens1) + float(trigg1)
                                                                                                                            i = i + 1
                                                                                                                            time.sleep(.2)
                                                                                                                        triggav1 = int(trigg1) / 11
                                                                                                                        print(f"triggered sensor 1 average = {triggav1}")
                                                                                                                        if float(triggav1) <= float(relav1) + float(error1):
                                                                                                                            print("RESULTS INVALID")
                                                                                                                        else:
                                                                                                                            print("RESULTS VALID")
                                                                                                            else:
                                                                                                                while r == 3:
                                                                                                                    import serial_comm
                                                                                                                    if __name__ == "__main__":
                                                                                                                        serial_comm.sensors()
                                                                                                                    if float(serial_comm.sens0) >= float(relav0) + float(error0) + .5:       # sensor 0
                                                                                                                        print("sensor 0 triggered")
                                                                                                                        print("starting")
                                                                                                                        r = 4
                                                                                                                        i = 0
                                                                                                                        while i <= 10:
                                                                                                                            import serial_comm
                                                                                                                            if __name__ == "__main__":
                                                                                                                                serial_comm.sensors()
                                                                                                                            trigg0 = float(serial_comm.sens0) + float(trigg0)
                                                                                                                            i = i + 1
                                                                                                                            time.sleep(.2)
                                                                                                                        triggav0 = int(trigg0) / 11
                                                                                                                        print(f"triggered sensor 0 average = {triggav0}")
                                                                                                                        if float(triggav0) <= float(relav0) + float(error0):
                                                                                                                            print("RESULTS INVALID")
                                                                                                                        else:
                                                                                                                            print("RESULTS VALID")


                                                                                                            print("Calibration complete!!")


                                                                                else:
                                                                                    if key == "serial speed":
                                                                                        print("speed options:")
                                                                                        print("within range 0 - 200 (BETA) (UNAVAILABLE)")
                                                                                        print("or AUTO (BETA) (UNAVAILABLE)")
                                                                                        ardspeed = input()

                                                                                        if ardspeed == "AUTO" or "auto":
                                                                                            print("starting RPi to Arduino 2 way collaboration")
                                                                                            if __name__ == '__main__':
                                                                                                ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
                                                                                                ser.reset_input_buffer()
                                                                                                while True:
                                                                                                    ser.write(b"auto\n")
                                                                                                    line = ser.readline().decode('utf-8').rstrip()
                                                                                                    print(line)
                                                                                                    time.sleep(1)
                                                                                        else:
                                                                                            print("starting RPi to Arduino 2 way collaboration")
                                                                                            if __name__ == '__main__':
                                                                                                ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
                                                                                                ser.reset_input_buffer()
                                                                                                while True:
                                                                                                    ser.write(f"{ardspeed}\n")
                                                                                                    line = ser.readline().decode('utf-8').rstrip()
                                                                                                    print(line)
                                                                                                    time.sleep(1)



                                                                                    else:
                                                                                        if key == "measurements":
                                                                                            for w in range(50):
                                                                                                import serial_comm
                                                                                                if __name__ == "__main__":
                                                                                                    serial_comm.sensors()
                                                                                                print(serial_comm.sens0)
                                                                                                print(serial_comm.sens1)
                                                                                                time.sleep(.1)






                                                                                                            
                                            
                                        

time.sleep(1)

