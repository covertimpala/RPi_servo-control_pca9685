import serial


ser=serial.Serial("/dev/ttyUSB0",9600)  #change ACM number as found from ls /dev/tty/ACM*
disallowed_characters = "rn\'"

while True:
    if(ser.in_waiting > 0):
        line = ser.readline()
        firs = str(line).replace("b'","")
        sec = str(firs).replace("r","")
        thir = str(sec).replace("\\n'","")
        final = str(thir).replace("\\","")
        print(final)
        
