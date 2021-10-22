import time
import subprocess
import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
from adafruit_servokit import ServoKit
from multiprocessing import Pool

import adafruit_motor.servo


# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)
kit.servo.frequency = 50
kit.servo[0].actuation_range = 180
kit.servo[1].actuation_range = 120
kit.servo[2].actuation_range = 130
kit.servo[3].actuation_range = 180  #still needs adjustment
kit.servo[4].actuation_range = 180  #still needs adjustment
kit.servo[5].actuation_range = 30   #range 30 = closed 10 = open
run = 0
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
            kit.servo[1].angle = angle

        else:
            if key == "exit":
                print("exiting")
                exit()

            else:
                if key == "idle":
                    print("going to idle pos")
                    kit.servo[0].angle = 180
                    time.sleep(2)
                    kit.servo[1].angle = 20
                    time.sleep(2)
                    kit.servo[2].angle = 15
                    time.sleep(2)
                    kit.servo[3].angle = 70
                    time.sleep(2)
                    kit.servo[4].angle = 140
                    time.sleep(2)
                    kit.servo[5].angle = 30
                    print("arm has been returned to idle pos")

                else:
                    if key == "2":
                        print("choose angle")
                        angle = int(input())
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

                                                else:
                                                    if key == "speed":
                                                        print("servo:")
                                                        servo = int(input())
                                                        print("angle:")
                                                        angle = int(input())
                                                        print("speed:")
                                                        speed = int(input())
                                                        speed_percent = round(speed / angle * 100)
                                                        print(speed_percent)
                                                        min_angle = angle / speed_percent
                                                        f = 1
                                                        while f in range(0, int(angle)):
                                                            print(f)
                                                            kit.servo[servo].angle = f
                                                            f = int(f + int(speed_percent))
                                                        kit.servo[servo].angle = angle
                                                            
                                            
                                        

time.sleep(1)

