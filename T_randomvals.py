import random
import time
i = 10
def randomvalue():
    global sens0
    sens0 = random.uniform(.5, 5)
    print(sens0)
    time.sleep(.2)