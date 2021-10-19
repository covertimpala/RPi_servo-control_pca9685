# RPi_servo-control_pca9685
raspberry pi 180° servo control using pca9685

### Requirements
Requires you to have the [adafruit servokit library](https://circuitpython.readthedocs.io/projects/servokit/en/latest/) installed

You also need to [configure i2c on your raspberry pi](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)

### Usage
Run `main.py` and type the pin number that the servo you wish to control is connected to eg. 0

Once you have done that it will reply with `choose angle`. Type the appropriate angle and hit enter, the selected servo should move to the specified angle.
