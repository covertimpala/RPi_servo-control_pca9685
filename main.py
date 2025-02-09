import time
import json
import board
#import colorama
from colorama import Fore
import busio
i2c = busio.I2C(board.SCL, board.SDA)
import math
from adafruit_servokit import ServoKit
#from multiprocessing import Pool
import multiprocessing
import RPi.GPIO as GPIO

try:
    from colorama import Fore
    nocolor = 0
except Exception:
    nocolor = 1

#import adafruit_motor.servo
#import serial

## Analog-digital converter setup
#import adafruit_pcf8591.pcf8591 as PCF
#from adafruit_pcf8591.analog_in import AnalogIn
#from adafruit_pcf8591.analog_out import AnalogOut
#i2c_2 = board.I2C()
#pcf = PCF.PCF8591(i2c_2)

#pcf_in_0 = AnalogIn(pcf, PCF.A0)
#pcf_out = AnalogOut(pcf, PCF.OUT)

#pcf_out.value = 65535
#raw_value = pcf_in_0.value
#scaled_value = (raw_value / 65535) * pcf_in_0.reference_voltage
#print("Pin 0: %0.2fV" % (scaled_value))
#print("")
##

#speech-to-text imports:
import speech_recognition as sr
global audio_sentence


GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 23
GPIO_ECHO = 24
LED = 18
RELAY = 17

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO . setup ( LED , GPIO . OUT )
GPIO.setup(RELAY, GPIO.OUT)
# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)
kit.servo.frequency = 50
kit.servo[0].actuation_range = 180
kit.servo[1].actuation_range = 120
kit.servo[2].actuation_range = 130 #adjust
kit.servo[3].actuation_range = 90  #still needs adjustment
kit.servo[4].actuation_range = 180  #still needs adjustment
kit.servo[5].actuation_range = 90   #range 50 = open 90 = closed
global run
global lock
r1 = 15
r2 = 7.9
r3 = 14.5
step = 2
run = 0
lock = 0
speed = 0
bypass = 1
_range = [-90, 90, -90, 90, -90, 90]
EMG = 0
global relav0
global relav1
global error0
def speech_to_text():
    global run
    global key
    print(Fore.RESET)
    #read duration from the arguments
    r = sr.Recognizer()
    mic = sr.Microphone()
    global audio
    global audio_sentence
    i = 0
    while i == 0:
        print("listening")
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            audio_sentence = r.recognize_google(audio)
            print(audio_sentence)
            if audio_sentence == "stop":
                run = 0
                i = 1
                tasks("")
            else:
                run = 1
                tasks(audio_sentence)
        except Exception as ex:
            print(ex)
            print(Fore.RED + "audio couldnt be recognised")
            print(Fore.RESET)

def idle():
    sp0 = multiprocessing.Process(target=spdcntrl,args=[0,200,180])
    sp1 = multiprocessing.Process(target=spdcntrl,args=[1,200,20])
    sp2 = multiprocessing.Process(target=spdcntrl,args=[2,200,0])
    sp3 = multiprocessing.Process(target=spdcntrl,args=[3,200,15])
    sp4 = multiprocessing.Process(target=spdcntrl,args=[4,200,140])
    sp5 = multiprocessing.Process(target=spdcntrl,args=[5,200,95])
    if __name__ == '__main__':
        sp0.start()
        sp1.start()
        sp2.start()
        sp3.start()
        sp4.start()
        sp5.start()
    print("done")
 #   print("going to idle pos")
  #  kit.servo[1].angle = 20
   # time.sleep(2)
    #kit.servo[2].angle = 0
    #time.sleep(2)
    #kit.servo[3].angle = 15
    #time.sleep(2)
    #kit.servo[0].angle = 180
    #time.sleep(2)
    #kit.servo[4].angle = 140
    #time.sleep(2)
    #kit.servo[5].angle = 95
    #print("arm has been returned to idle pos")

def id_t(serv):
    if serv == "0":
        spdcntrl(0,200,180)
        #kit.servo[0].angle = 180
    elif serv == "1":
        spdcntrl(1,200,20)
        #kit.servo[1].angle = 20
    elif serv == "2":
        spdcntrl(2,200,0)
        #kit.servo[2].angle = 5
    elif serv == "3":
        spdcntrl(3,200,15)
        #kit.servo[3].angle = 25
    elif serv == "4":
        spdcntrl(4,200,140)
        #kit.servo[4].angle = 140
    elif serv == "5":
        spdcntrl(5,200,95)
        #kit.servo[5].angle = 95

def spdcntrl(selserv, stp, an): #servo, step, angle
    curran = round(int(kit.servo[selserv].angle))
    an_n = (an-curran)/stp
    for z in range(stp):
        if z != 0:
            #print(z, z*an/stp)
            kit.servo[selserv].angle = curran+z*an_n
            time.sleep(0.01)

#========================================================================================================================#
################################################### Inverse Kinematics ###################################################
#========================================================================================================================#

def calculateab(locx, locy, o, r1, r2, r3, _range, bypass, x_dist, y_dist):
    b = math.pi - math.acos((-locx**2 - locy**2 + r1**2 + r2**2) / (2*r1*r2))#(r1**2+r2**2)            (2*r1*r2)
    #print("b:", b)
    bt = math.degrees(b)
    if bt >= _range[2]*bypass and bt <=_range[3]*bypass:
        a = -math.asin((r2*math.sin(b))/((locx**2 + locy**2)**(1/2)))+math.asin((locx)/((locx**2 + locy**2)**(1/2)))
        #print("a:", a)
        at = math.degrees(a)
        if at >= _range[0]*bypass and at <=_range[1]*bypass:
            ys = (((locy-r1*math.cos(a))/(locx-r1*math.sin(a)))*(x_dist-r1*math.sin(a))+r1*math.cos(a)) #equation of the line from r2
            ds = math.sqrt((x_dist-locx)**2 + (ys-locy)**2) #side 1
            ds3 = abs(ys-y_dist) #side 3
            c = math.degrees(math.acos((ds**2+r3**2-ds3**2)/(2*ds*r3))) #Cosine rule
            if x_dist < locx:
                cp = c-180
                if cp >= _range[4]*bypass and cp <= _range[5]*bypass:
                    if nocolor == 0:
                        print(Fore.RED + "Additional", o) #Uncertain has been updated to "Additional"
                        print(Fore.RESET + "",at,bt,c, "or", cp)
                        return [at, bt, c, "a"]
                    else:
                        print("Additional", o)
                        print(at,bt,cp)
                        return [at, bt, c, "a"]
                else:
                    #print(Fore.RED + "angle out of range" + Fore.RESET)
                    return ("out of range")
            elif c >= _range[4] and c <=_range[5]:
                if nocolor == 0:
                    print(Fore.GREEN + "Point on circle (angle degrees):", o, "location:", locx, locy)
                    print(Fore.RESET + "Degrees:",at,bt,c)
                    return [at, bt, c, ""]
                else:
                    print("Point on circle (angle degrees):", o, "location:", locx, locy)
                    print("Degrees:",at,bt,c)
                    return [at, bt, c, ""]
        else:
            #print(Fore.RED + "angle out of range" + Fore.RESET)
            return ("out of range")
    else:
        #print(Fore.RED + "angle out of range" + Fore.RESET)
        #print()
        return ("out of range")

def choosepos(segment1, segment2, segment3, x_dist, y_dist, step, _range, bypass, offstx_, offsty_, simpl, z):
    if simpl == False:
        x_p = offstx_
        y_p = offsty_
    else:
        x_p = r3*math.cos(math.radians(z/step))#r3*math.cos(math.radians(i))
        y_p = r3*math.sin(math.radians(z/step))#r3*math.sin(math.radians(i))
    joint3loc = [x_dist+x_p, y_dist+y_p]
    try:
        return(calculateab(joint3loc[0], joint3loc[1],"", segment1, segment2, segment3, _range, bypass, x_dist, y_dist))
    except Exception as f:
        print("failed:", f)
        #print(Fore.RED + "OUT OF RANGE", i/step, joint3loc[0], joint3loc[1])
        #continue

#========================================================================================================================#
################################################# Inverse Kinematics END #################################################
#========================================================================================================================#
    
def dista(q,n):
    GPIO.output(GPIO_TRIGGER, True)

    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
    #while True:
        #if GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
            #break
        #else:
            #if time.time() - StartTime > 1:
                #StopTime = StartTime + 1
                #break
            

    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    q.value=distance
    #return distance

def distance():
    tm = multiprocessing.Value('d', 0)
    q = multiprocessing.Queue() ###########################################################################
    #ds = multiprocessing.Process(target=dista, args=(q))
    ds = multiprocessing.Process(target=dista, args=(tm,1))
    if __name__ == '__main__':
        ds.start()
    strtm = time.time()
    global miii
    while time.time() - strtm() < 1:
        miii=q.get()
        if miii != None:
            break
    if miii != None:
        return miii
    else:
        return distance()
        

def tasks(insval):
    global run
    global audio_sentence
    global key
    global lock
    while run <= 10:
        if run == 0:
            key = input()
        else:
            if run == 1:
                key = insval
        key = key.lower()
        if key == "0":
            print("choose angle")
            angle = int(input())
            kit.servo[0].angle = angle
            

        elif key == "1":
            print("choose angle")
            angle = int(input())
            
            if lock == 1:
                change_angle = int(angle) - int(round(int(kit.servo[1].angle)))
                kit.servo[1].angle = angle
                if int(round(int(kit.servo[2].angle) + int(change_angle))) >= 0:
                    if int(round(int(kit.servo[2].angle) + int(change_angle))) <= kit.servo[2].actuation_range:
                        kit.servo[2].angle = int(round(int(kit.servo[2].angle) + int(change_angle)))
                        print(int(change_angle))
                        print(round(kit.servo[2].angle + change_angle))
                    else:
                        kit.servo[2].angle = kit.servo[2].actuation_range
                        print("cant engage lock")
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

        elif key == "exit":
            print("exiting")
            GPIO.output(GPIO_TRIGGER, False)
            GPIO.cleanup()
            exit()

        #elif key == "idle":
            
         #   idle()


        elif key == "2":
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
                                    
                                

        elif key == "3":
            print("choose angle")
            angle = int(input())
            kit.servo[3].angle = angle


        elif key == "4":
            print("choose angle")
            angle = int(input())
            kit.servo[4].angle = angle


        elif key == "5":
            print("choose angle")
            angle = int(input())
            kit.servo[5].angle = angle


        elif key == "test":
            print("this function is no longer available")


        elif key == "angle":
            print("insert servo num")
            servo_val = int(input())
            servo_angle = kit.servo[servo_val].angle
            print(f"servo {servo_val} angle ≈ {round(servo_angle)}")


        elif key == "range":
            print("")
            print("================================================")
            print("=========== angle ranges for servos ============")
            print("================================================")
            print("")
            print(f"servo [0] = 00° - {kit.servo[0].actuation_range}°")
            print(f"servo [1] = 00° - {kit.servo[1].actuation_range}°")
            print(f"servo [2] = 00° - {kit.servo[2].actuation_range}°") #update
            print(f"servo [3] = 00° - {kit.servo[3].actuation_range}°")
            print(f"servo [4] = 00° - {kit.servo[4].actuation_range}°")
            print(f"servo [5] = 50° - {kit.servo[5].actuation_range}°")


        elif key == "help":
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
            print("turn on/off led:")
            print("led <on/off>")
            print("")
            print("activate/deactivate EMG sensors:  **(not included in this package)**")
            print("emg <on/off>")
            print("")
            print("scan surroundings:")
            print("scan")
            print("scan for new objects:")
            print("rescan/search")
                    


        elif key == "led on":
            GPIO.output(18, True)
            print("led is on")


        elif key == "led off":
            GPIO.output(18, False)
            print("led is off")


        elif key == "lock":
            print("servo to lock (2 or 3)")
            servo_lock = int(input())
            if servo_lock == 2:
                lock = 1

            else:
                if servo_lock == 3:
                    lock = 2

            print("sucess!!")
                    


        elif key == "unlock":
            print("unlocking servos")
            lock = 0
            print("servo(s) unlocked")


        elif key == "scan" or key == "look": ####################################
            print("preparing scan")
            kit.servo[0].angle = 0
            idle()
            kit.servo[0].angle = 180
            print("checking systems")
            kit.servo[4].angle = 35
            test = round(distance(),2) ###########
            print(test)
            startt = time.time()
            while True:
                test = round(distance(),2) ###########
                print(test)
                if test <= 10 or test >= 3000:
                    global total_t
                    endt = time.time()
                    total_t = endt - startt
                    print("total time: ", round(total_t, 3))
                    print("systems scan valid")
                    kit.servo[4].angle = 140
                    break
                else:
                    print("retrying")
                    continue
            print("preparing json")
            open("sonicmes.json", "w").close()
            global mes
            mes = {}
            with open("sonicmes.json", "r+") as sonicmes:
                print("starting scan")
                for p in range(8):
                    for q in range(180):
                        kit.servo[0].angle = 180 - q
                        time.sleep(.01)
                    #print(p)
                    kit.servo[2].angle = p * 2 + 5
                    print("starting layer", p + 1)
                    for g in range(45):
                        kit.servo[0].angle = g * 4
                        time.sleep(.043) #total_t
                        dist = distance()
                        mes[str(p) + str(g)] = round(dist,2)
                        #print(str(p) + str(g))
                        print(round(dist),2)
                        
                print(mes)
                sonicmes.seek(0)
                json.dump(mes, sonicmes)
                sonicmes.truncate
            print("scan complete!")
            idle()


        elif key == "dist" or key == "distance":
            print(round(distance(),2))


        elif key == "rescan" or key == "search":
            print("Preparing json")
            global objects
            objects = {}
            open("objects.json", "w").close()
            print("Opening json")
            with open("sonicmes.json", "r+") as base_file:
                base = json.load(base_file)
                print(base["00"])
                for th in range(8):
                    for rt in range(180):
                        kit.servo[0].angle = 180 -rt
                        time.sleep(.01)
                    kit.servo[2].angle = th * 2 + 5
                    print("starting layer", th + 1)
                    for yt in range(45):
                        kit.servo[0].angle = yt * 4
                        dist = distance()
                        #print(base[str(th) + str(yt)])
                        if dist <= base[str(th) + str(yt)] + 17 and dist >= base[str(th) + str(yt)] - 17:
                            print("maching results")
                        else:
                            if dist < 70:
                                if dist > base[str(th) + str(yt)] + 17:
                                    print("object has been moved")
                                else:
                                    print("new object detected")
                                    objects[str(th), str(yt * 4)] = dist
                            else:
                                print("result out of range")
                        time.sleep(.043)
            
            idle()
            print("processing objects")
            objectangles = {}
            
            for lev in range(8):
                print("starting level", lev)
                for ang in range(180):
                    try:
                        print(ang,":" ,objects[str(lev), str(ang)])
                        try:
                            objectangles[ang] = objectangles[ang] + 1
                        except:
                            objectangles[ang] = 1
                    except:
                        continue
            global objectstreak
            global objectss
            global acob
            objectstreak = {}
            objectss = {}
            acob = {}
            for tanfdg in range(45):
                try:
                    print(tanfdg * 4,":" ,objectangles[tanfdg * 4])
                    if objectangles[tanfdg * 4] >= 2:
                            if prev == "yes":
                                objectstreak[len(objectstreak)] = objectstreak[len(objectstreak)] + 1
                            else:
                                objectstreak[len(objectstreak) + 1] = 1
                                prev = "yes"
                                objectss[len(objectstreak)] = tanfdg * 4
                    else:
                        prev = "no"
                except:
                    prev  = "no"
                    continue
            print(objectstreak)
            print(objectss)
            for fer in range(len(objectstreak)):
                if objectstreak[fer + 1] >= 3:
                    acob[len(acob) + 1] = fer + 1


        elif key == "text to speech" or key == "mic on":
            run = 1
            speech_to_text()


        elif key == "power on":
            GPIO.output(RELAY, GPIO.HIGH)
            print("relay on")


        elif key == "power off":
            GPIO.output(RELAY, GPIO.LOW)
            print("relay off")
                        

        elif "object" in key:
            print("calculating objects")
            global ob
            ob = key[len(key)-1]
            try:
                int(ob)
                print("calculating")
                print("object location: ", objectss[acob[int(ob)]], "to", (((objectstreak[acob[int(ob)]] - 1)*4) + objectss[acob[int(ob)]]))
                print("aiming at object")
                kit.servo[0].angle = (((objectstreak[acob[int(ob)]] - 1)*4) + objectss[acob[int(ob)]] + objectss[acob[int(ob)]])/2
                print("objects approx width")
                
                
            except Exception as exexe:
                print("object not specified or search/rescan not complete")
                print("error: ", exexe)
                print("do you want to see available objects?  y/n")
                query = input()
                if query == "y" or query == "yes":
                    try:
                        objectss
                        print("available objects are: ", acob)
                        print("reference: <object label>: <program ref>")
                    except:
                        print("search/rescan must be done before this feature can be used")

        elif "idle_t" in key:
            #id_t("0")
            p0 = multiprocessing.Process(target=spdcntrl,args=[0,200,180])
            p1 = multiprocessing.Process(target=spdcntrl,args=[1,200,20])
            p2 = multiprocessing.Process(target=spdcntrl,args=[2,200,0])
            p3 = multiprocessing.Process(target=spdcntrl,args=[3,200,15])
            p4 = multiprocessing.Process(target=spdcntrl,args=[4,200,140])
            p5 = multiprocessing.Process(target=spdcntrl,args=[5,200,95])
            if __name__ == '__main__':
                p0.start()
                p1.start()
                p2.start()
                p3.start()
                p4.start()
                p5.start()
            print("done")
        
        elif "speed" in key:
            print("servo num?")
            selserv = int(input())
            print("steps")
            stp = int(input())
            print("angle")
            an = int(input())
            curran = round(int(kit.servo[selserv].angle))
            an_n = (an-curran)/stp
            for z in range(stp):
                if z != 0:
                    #print(z, z*an/stp)
                    kit.servo[selserv].angle = curran+z*an_n
                    time.sleep(0.01)
            print("done")

        elif "inv_k" in key:
            an_a = math.radians(kit.servo[1].angle)
            an_b = math.radians(kit.servo[2].angle)
            an_c = math.radians(kit.servo[3].angle)
            print(Fore.BLUE + "destination x-dist (cm)" + Fore.RESET)
            d_x = int(input())
            print(Fore.BLUE + "destination y-dist (cm)" + Fore.RESET)
            d_y = int(input())
            destination = [d_x,d_y]
            currpos = [r1*math.sin(an_a)+r2*math.sin(an_a+an_b)+r3*math.sin(an_a+an_b+an_c),r1*math.cos(an_a)+r2*math.cos(an_a+an_b)+r3*math.cos(an_a+an_b+an_c)]
            #steps = 200
            path = [destination[0] - currpos[0], destination[1] - currpos[1]]
            print(path)
            offstx = -r3*math.sin(an_a+an_b+an_c) #currpos[0]-r3*math.sin(an_c)
            offsty = -r3*math.cos(an_a+an_b+an_c) #currpos[1]-r3*math.cos(an_c)
            print(offstx, offsty)

            abcang = choosepos(r1, r2, r3, destination[0], destination[1], step, _range, bypass, offstx, offsty, False, 1)
            print(abcang)
            if abcang != "out of range":
                #dan_a = math.degrees(an_a)
                #dan_b = math.degrees(an_b)
                #dan_c = math.degrees(an_c)
                m1 = multiprocessing.Process(target=spdcntrl,args=[1,200,(abcang[0])]) # +- 90
                m2 = multiprocessing.Process(target=spdcntrl,args=[2,200,(abcang[1])]) # +- 90
                m3 = multiprocessing.Process(target=spdcntrl,args=[3,200,(abcang[2])])
                if __name__ == '__main__':
                    m1.start()
                    m2.start()
                    m3.start()
                print("moving to point")

            else:
                print(Fore.CYAN + "Check for closest match? (y/n)")
                print("(this will shift the locked segment)")
                an_s = input()
                if an_s == "y" or an_s == "yes":
                    print(Fore.GREEN + "finding closest match" + Fore.RESET)
                    #print(chsp(r1, r2, r3, x_dist, y_dist, step, _range, bypass, ))
                    liovar = {}
                    for z in range(359*step):
                        va = choosepos(r1, r2, r3, destination[0], destination[1], step, _range, bypass, offstx, offsty, True, z)
                        if va != "out of range" and va != None:
                            liovar[len(liovar)] = z,va
                    print(liovar)
                    print(liovar[1][0])
                    cv = -5
                    thetax = round(math.asin(offstx/r3),5)
                    thetay = round(math.acos(offsty/r3),5)
                    print(thetax, thetay)
                    if abs(thetax) == abs(thetay):
                        sol = math.degrees(abs(thetax))
                    else:
                        print("Something went wrong")
                    for p in range(len(liovar)):
                        print(p)
                        ck_ = liovar[p][0]/sol
                        if abs(ck_) < abs(cv):
                            cv = ck_
                            ck = liovar[p][0]
                            pval = p
                    print(sol)
                    print(ck)
                    print(ck_)
                    m1 = multiprocessing.Process(target=spdcntrl,args=[1,200,(liovar[pval][1][0])]) # +- 90
                    m2 = multiprocessing.Process(target=spdcntrl,args=[2,200,(liovar[pval][1][1])]) # +- 90
                    m3 = multiprocessing.Process(target=spdcntrl,args=[3,200,(liovar[pval][1][2])]) # +- 90
                    if __name__ == '__main__':
                        m1.start()
                        m2.start()
                        m3.start()
                    print("moving to point")


        else:
            print("unrecognised command")

        if run == 1:
            run = 20


tasks("")
