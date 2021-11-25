import time
import subprocess
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
                                                                            
                                                                            time.sleep(2)
                                                                            while EMG == 1:
                                                                                import serial_comm
                                                                                if __name__ == "__main__":
                                                                                    serial_comm.sensors()
                                                                                    print(serial_comm.sens0)
                                                                                    print(serial_comm.sens1)
                                                                                
                                                                                


                                                                        else:
                                                                            if key == "emg off":
                                                                                EMG = 0
                                                                                print("sensors deactivated")
                                                                            
                                                                                    
                                                                                
                                                                            


                                                                    

                                                            
                                                        
                                                            
                                            
                                        

time.sleep(1)

