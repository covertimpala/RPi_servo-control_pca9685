import serial
import time


ser=serial.Serial("/dev/ttyUSB0",9600)  #change ACM number as found from ls /dev/tty/ACM*
time.sleep(3)

while True:
    if(ser.in_waiting > 0):
        line = ser.readline()  #reads serial communications
        firs = str(line).replace("b'","")   #removing characters from data
        sec = str(firs).replace("r","")     #
        thir = str(sec).replace("\\n'","")  #
        final = str(thir).replace("\\","")  #
        processed = final.split(',')
        sens0 = processed[0]
        sens1 = processed[1]
        
        
