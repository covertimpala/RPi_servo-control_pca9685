
import serial

ser=serial.Serial("/dev/ttyUSB0",9600)  #change ACM number as found from ls /dev/tty/ACM*
def sensors():
    line = ser.readline()  #reads serial communications
    firs = str(line).replace("b'","")   #removing characters from data
    sec = str(firs).replace("r","")     #
    thir = str(sec).replace("\\n'","")  #
    final = str(thir).replace("\\","")  #
    processed = final.split(',')
    global sens0
    global sens1
    sens0 = processed[0]
    sens1 = processed[1]

        
        
