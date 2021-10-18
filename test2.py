
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Example that iterates through a servo on every channel, sets each to 180 and then back to 0."""
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
kit.servo[5].actuation_range = 25   #range 25 = closed 15 = open
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
                                        

time.sleep(1)

