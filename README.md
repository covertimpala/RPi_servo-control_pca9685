# RPi_servo-control_pca9685
raspberry pi 180° servo control using pca9685

### Requirements
Requires you to have the [adafruit servokit library](https://circuitpython.readthedocs.io/projects/servokit/en/latest/) installed

You also need to [configure i2c on your raspberry pi](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)

### Usage
Run `main.py` and type the number of the pin that the servo you wish to control is connected to eg. 0

Once you have done that it will reply with `choose angle`. Type the appropriate angle and hit enter, the selected servo should move to the specified angle.


### EMG
EMG (Electromyography) is used to measure the muscles response to electrical signals.
In this project the EMG signals are used to control a robotic arm.

### Setup:

The setup used here is an Arduino Uno, RPi, two myoware EMG sensors and a PCA9685 along with six servos labeled 0 - 5.

Upload the measurements.ino file to the Arduino and connect the myoware sensors to pins A0 and A1.

Once that is complete activate the RPi and install the files from this repository.

Open the terminal on the RPi and type `ls /dev/tty*`, then plug the Arduino Uno to the RPi using a USB cable and repeat the command. Find the device that should now have appeared and remember it!

Open serial_comm.py and replace `/dev/ttyUSB0` with the name you got.

Run serial_comm.py and check if any errors occur.

(if you encounter an error please read [this tutorial](https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/))

