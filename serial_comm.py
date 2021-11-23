import serial


ser=serial.Serial("/dev/ttyUSB0",9600)  #change ACM number as found from ls /dev/tty/ACM*


while True:
    if(ser.in_waiting > 0):
        line = ser.readline()
        print(line)
        
