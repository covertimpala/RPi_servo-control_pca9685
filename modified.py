import pygame
import math
import time
import board
import busio
import multiprocessing
i2c = busio.I2C(board.SCL, board.SDA)
from adafruit_servokit import ServoKit
from gpiozero import LED, OutputDevice, DistanceSensor
import os
os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

RELAY = 17
relay = OutputDevice(RELAY)

kit = ServoKit(channels=16)
kit.servo.frequency = 50
kit.servo[0].actuation_range = 180
kit.servo[1].actuation_range = 120
kit.servo[2].actuation_range = 130 #adjust
kit.servo[3].actuation_range = 90  #still needs adjustment
kit.servo[4].actuation_range = 180  #still needs adjustment
kit.servo[5].actuation_range = 70   #range 40 = open 70 = closed

pygame.init()

dec_p = 2

target_p = [10,10, 0, 130, 50, 40] # x, y, rotation of joint 1, solution (position of joint 4 around target), claw, joint 5 rotation


try:
    from colorama import Fore
    nocolor = 0
except Exception:
    nocolor = 1

r1 = 15 #Length of segment 1 of the arm (between joints a and b (1 and 2))
r2 = 7.9 #Length of segment 2 of the arm (between joints b and c (2 and 3))
r3 = 14.5 #Length of segment 3 of the arm (between joints c (3) and end effector)
scale_factor = 10 #scale the simulated arm
offsets = [50, 90, 30]
modifiers = [1,-1,-1]
#global bthld
bthld = 0
#global togglemode
#togglemode = 0
#x_dist = 18
#y_dist = 20
#step = 2 #359*step|| used to determine the number of points to check
bypass = 5 #switch to  a value >= 4 to bypass filter
_range = [-90, 90] #angle ranges (anything outside the range is filtered out (as long as bypass = 1))
#sol = 170
#Degorrad = "deg" # choose between "deg" or "rad" (degrees or radians for output)
#global joy_inv_k
#joy_inv_k = [0,0,0]
def cleanup():
    #trigger.close()
    relay.close()
    print("GPIO cleanup done")

def toggle_relay():
    relay.toggle()
    print("Relay toggled")

def move_servos(a0, a1, a2, a3, a4, a5):
    try:
        an1 = a1*modifiers[0]+offsets[0]
        an2 = a2*modifiers[1]+offsets[1]
        an3 = a3*modifiers[2]+offsets[2]
        print(an1, an2, an3)
        if an3 > 20:
            an3 = 20
        #splist = []
        #splist.append(multiprocessing.Process(target=servmov,args=[0,a0]))
        #splist.append(multiprocessing.Process(target=servmov,args=[1,an1]))
        #splist.append(multiprocessing.Process(target=servmov,args=[2,an2]))
        #splist.append(multiprocessing.Process(target=servmov,args=[3,an3]))
        #splist.append(multiprocessing.Process(target=servmov,args=[4,a4]))
        #splist.append(multiprocessing.Process(target=servmov,args=[5,a5]))

        sp0 = multiprocessing.Process(target=servmov,args=[0,a0])
        sp1 = multiprocessing.Process(target=servmov,args=[1,an1])
        sp2 = multiprocessing.Process(target=servmov,args=[2,an2])
        sp3 = multiprocessing.Process(target=servmov,args=[3,an3])
        sp4 = multiprocessing.Process(target=servmov,args=[4,a4])
        sp5 = multiprocessing.Process(target=servmov,args=[5,a5])
        

        #for i in range(splist):
         #   print(i)
          #  try:
           #     splist[i].start()
            #except Exception as e:
             #   print(e)
        sp0.start()
        sp1.start()
        sp2.start()
        sp3.start()
        sp4.start()
        sp5.start()
    except Exception as e:
        print(e)

def servmov(servo, angle):
    try:
        kit.servo[servo].angle = angle
    except Exception as e:
        print(e)

def verify(a,b,c):
    try:
        px =round(r1*math.sin(a)+r2*math.sin(a+b)+r3*math.sin(a+b+c),2)
        py =round(r1*math.cos(a)+r2*math.cos(a+b)+r3*math.cos(a+b+c),2)
        return([px,py])
    except Exception:
        return([0,0])

def calculateab(locx, locy, o, _range, bypass, x_dist, y_dist):
    b = math.pi - math.acos((-locx**2 - locy**2 + r1**2 + r2**2) / (2*r1*r2))#(r1**2+r2**2)            (2*r1*r2)
    #print("b:", b)
    bt = math.degrees(b)
    if bt >= _range[0]*bypass and bt <=_range[1]*bypass:
        a = -math.asin((r2*math.sin(b))/((locx**2 + locy**2)**(1/2)))+math.asin((locx)/((locx**2 + locy**2)**(1/2)))
        #print("a:", a)
        at = math.degrees(a)
        if at >= _range[0]*bypass and at <=_range[1]*bypass:
            ys = (((locy-r1*math.cos(a))/(locx-r1*math.sin(a)))*(x_dist-r1*math.sin(a))+r1*math.cos(a)) #equation of the line from r2
            ds = math.sqrt((x_dist-locx)**2 + (ys-locy)**2) #side 1
            ds3 = abs(ys-y_dist) #side 3
            ct = math.acos((ds**2+r3**2-ds3**2)/(2*ds*r3))
            c = math.degrees(ct) #Cosine rule
            cp = math.pi-ct#-180
            #px =round(r1*math.sin(at)+r2*math.sin(at+bt)+r3*math.sin(at+bt+c),2)
            #py =round(r1*math.cos(at)+r2*math.cos(at+bt)+r3*math.cos(at+bt+c),2)
            #print(f"[{verify(at,bt,c)}] == [{x_dist, y_dist}]")
            #print(f"[{verify(at,bt,-c)}] == [{x_dist, y_dist}]")

            # Verification of the output values
            if verify(a,b,ct)[0] == round(x_dist,2) and verify(a,b,ct)[1] == round(y_dist,2):
                return([a,b,ct])
            elif verify(a,b,-ct)[0] == round(x_dist,2) and verify(a,b,-ct)[1] == round(y_dist,2):
                return([a,b,-ct])
            elif verify(a,b,cp)[0] == round(x_dist,2) and verify(a,b,cp)[1] == round(y_dist,2):
                return([a,b,cp])
            elif verify(a,b,-cp)[0] == round(x_dist,2) and verify(a,b,-cp)[1] == round(y_dist,2):
                return([a,b,-cp])

            else:
                #print("no solution")
                return("no solution")
            #if x_dist < locx:
                
             #   if cp >= _range[0]*bypass and cp <= _range[1]*bypass:
              #      if nocolor == 0:
               #         print(Fore.RED + "Additional", o) #Uncertain has been updated to "Additional"
                #        print(Fore.RESET + "",at,bt,c, "or", cp)
                 #   else:
                  #      print("Additional", o)
                   #     print(at,bt,cp)
            #elif c >= _range[0] and c <=_range[1]:
             #   if nocolor == 0:
              #      print(Fore.GREEN + "Point on circle (angle degrees):", o, "location:", locx, locy)
               #     #print(Fore.RESET + "Degrees:",at,bt,c)
                #else:
                 #   print("Point on circle (angle degrees):", o, "location:", locx, locy)
                    #print("Degrees:",at,bt,c)
            #return([at,bt,c])

def choosepos(x_dist, y_dist, _range, bypass, sol):
    #angle = random.randrange(0,359,1)
    #for i in range(359*step):
    #print(i/step)
    #print("wtf")
    x_p = r3*math.cos(math.radians(sol))#r3*math.cos(math.radians(i))
    y_p = r3*math.sin(math.radians(sol))#r3*math.sin(math.radians(i))
    joint3loc = [x_dist+x_p, y_dist+y_p]
    #print(joint3loc)
    try:
        return(calculateab(joint3loc[0], joint3loc[1], sol, _range, bypass, x_dist, y_dist))
    except Exception as f:
        print(f)
        #print(Fore.RED + "OUT OF RANGE", i/step, joint3loc[0], joint3loc[1])
        #continue

#print(choosepos(r1, r2, r3, x_dist, y_dist, step, _range, bypass, sol))


class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, (0, 0, 0))
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10



def main():
    global btoggle2
    # Set the width and height of the screen (width, height), and name the window.
    togglemode = 0
    global bthld
    #bthld = 0
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Joystick example")
    global joy_inv_k
    joy_inv_k = 0

    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # Get ready to print.
    text_print = TextPrint()

    # This dict can be left as-is, since pygame will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    joysticks = {}

    done = False
    while not done:
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        if 0 < target_p[5] + bthld < 180:
            target_p[5] += bthld
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.
            
            mvmnt = 0

            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
                if event.button == 0:
                    #joystick = joysticks[event.instance_id]
                    #if joystick.rumble(0.7, 1, 500):
                    #    print(f"Rumble effect played on joystick {event.instance_id}")
                    if togglemode < 2:
                        togglemode += 1
                    else:
                        togglemode = 0

                elif event.button == 2:
                    #if btoggle2 == 0:
                    print("relay bttn pressed")
                    toggle_relay()
                        #btoggle2 = 1
                        #mp1 = multiprocessing.Process(target=buttontimeout)
                        #mp1.start()



                elif event.button == 4:
                    #target_p[5] -= 0.5
                    bthld = -0.5
                    mvmnt = 1
                elif event.button == 5:
                    #target_p[5] += 0.5
                    bthld = 0.5
                    mvmnt = 1
                #else:
                    #bthld = 0
            

            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")
                if event.button == 4 or event.button == 5:
                    #target_p[5] -= 0.5
                    bthld = 0
            

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        # Drawing step
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill((255, 255, 255))
        text_print.reset()

        # Get count of joysticks.
        joystick_count = pygame.joystick.get_count()

        text_print.tprint(screen, f"Number of joysticks: {joystick_count}")
        text_print.indent()

        # For each joystick:
        for joystick in joysticks.values():
            jid = joystick.get_instance_id()

            text_print.tprint(screen, f"Joystick {jid}")
            text_print.indent()

            # Get the name from the OS for the controller/joystick.
            name = joystick.get_name()
            text_print.tprint(screen, f"Joystick name: {name}")

            guid = joystick.get_guid()
            text_print.tprint(screen, f"GUID: {guid}")

            power_level = joystick.get_power_level()
            text_print.tprint(screen, f"Joystick's power level: {power_level}")

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other. Triggers count as axes.
            axes = joystick.get_numaxes()
            text_print.tprint(screen, f"Number of axes: {axes}")
            text_print.indent()
            
            global sft
            sft = {}
            for i in range(axes):
                axis = joystick.get_axis(i)
                text_print.tprint(screen, f"Axis {i} value: {axis:>6.3f}")
                #print(axis)
                
                if i == 0: #J1 x-axis
                    if axis > 0.2 or axis < -0.1:
                        #target_p[0] += -1*round(axis/5,dec_p)
                        #sft[3] = round(axis/5,dec_p)
                        if 0 < target_p[2] + round((axis),dec_p) <= 180:
                            target_p[2] += round((axis),dec_p)
                        mvmnt = 1
                    else:
                        #mvmnt = 1
                        sft[0] = 0
                if i == 1: #J1 y-axis
                    if axis > 0.02 or axis < -0.19:
                        target_p[1] += round(-1*axis/5,dec_p)
                        sft[1] = -1*round(-1*axis/5,dec_p)
                        mvmnt = 1
                    else:
                        #mvmnt = 1
                        sft[1] = 0
                if i == 2 and togglemode != 1: #J2 x-axis ------->> Claw
                    if axis > 0.12:
                        if target_p[4] + round(axis/2,dec_p) >=30 and target_p[4] + round(axis/2,dec_p) <= 70:
                            target_p[4] += round(axis/2,dec_p)
                            mvmnt = 1
                        else:
                            time.sleep(0.2)
                            joystick.rumble(0.7, 1, 10)
                            time.sleep(0.2)
                            joystick.stop_rumble()
                            #time.sleep(0.5)
                            #joystick.rumble(0.7, 1, 10)
                        #print("x-motion")
                if i == 3 and togglemode != 2: #J2 y-axis ------->> position of joint 4 around target point
                    if axis > 0 or axis < -0.19:
                        target_p[3] += round(-1*axis/2,dec_p)
                        sft[2] = round(axis/2,dec_p)
                        mvmnt = 1
                    else:
                        #mvmnt = 1
                        sft[2] = 0
                elif togglemode == 2:
                    sft[2] = 0
                        #print("y-motion")
                if i == 4: #trigger 1 (LT)
                    #if target_p[2] - round((axis + 1)/2,dec_p) >= 0:
                     #   target_p[2] -= round((axis + 1)/2,dec_p)
                    if axis > 0.2 or axis < -0.1:
                        target_p[0] += -1*round(axis/5,dec_p)
                        sft[0] = round(axis/5,dec_p)
                        mvmnt = 1
                    else:
                        #mvmnt = 1
                        sft[0] = 0
                if i == 5 and togglemode != 1: #trigger 2 (RT)
                    if axis > 0.12:
                        #if target_p[2] + round((axis + 1)/2,dec_p) <= 180:
                        #    target_p[2] += round((axis + 1)/2,dec_p)
                        axis = axis*(-1)
                        if 30 <= target_p[4] + round(axis/2,dec_p) <= 70:
                            target_p[4] += round(axis/2,dec_p)
                            mvmnt = 1


            #if event.type == pygame.JOYAXISMOTION:
            if mvmnt == 1:
                print(mvmnt)
                #global joy_inv_k
                #joy_inv_k = {}
                joy_inv_k = choosepos(target_p[0], target_p[1], _range, bypass, target_p[3])
                    #rmbr1 = joy_inv_k[0]
                    #rmbr2 = joy_inv_k[1]
                    #rmbr3 = joy_inv_k[2]
                
            #print(joy_inv_k)
            #joy_inv_k = [rmbr1, rmbr2, rmbr3]
            #print("r: ", rmbr1, "mv: ", mvmnt)
            
            pygame.draw.circle(screen, (4, 12, 191, 0.8), (500-target_p[0]*scale_factor, 700-target_p[1]*scale_factor),4)
            pygame.draw.rect(screen, (180, 147, 217, 0.8), pygame.Rect(670,70,10*scale_factor,6*scale_factor))
            for aa in range(togglemode+1):
                pygame.draw.circle(screen, (4, 12, 191, 0.8), (700 + aa*20, 100),6)

            if joy_inv_k != 0 and joy_inv_k != None and joy_inv_k != "no solution":
                ### DRAWING ARM REPRESENTATION ###
                pygame.draw.line(screen, (191, 4, 4, 0.8), (500,700), (500-r1*math.sin(joy_inv_k[0])*scale_factor, 700-r1*math.cos(joy_inv_k[0])*scale_factor), 2)
                pygame.draw.line(screen, (191, 179, 4, 0.8), (500-r1*math.sin(joy_inv_k[0])*scale_factor, 700-r1*math.cos(joy_inv_k[0])*scale_factor), (500-(r1*math.sin(joy_inv_k[0])+r2*math.sin(joy_inv_k[0]+joy_inv_k[1]))*scale_factor, 700-(r1*math.cos(joy_inv_k[0])+r2*math.cos(joy_inv_k[0]+joy_inv_k[1]))*scale_factor), 2)
                pygame.draw.line(screen, (8, 191, 4, 0.8), (500-(r1*math.sin(joy_inv_k[0])+r2*math.sin(joy_inv_k[0]+joy_inv_k[1]))*scale_factor, 700-(r1*math.cos(joy_inv_k[0])+r2*math.cos(joy_inv_k[0]+joy_inv_k[1]))*scale_factor), (500-(r1*math.sin(joy_inv_k[0])+r2*math.sin(joy_inv_k[0]+joy_inv_k[1])+r3*math.sin(joy_inv_k[0]+joy_inv_k[1]+joy_inv_k[2]))*scale_factor, 700-(r1*math.cos(joy_inv_k[0])+r2*math.cos(joy_inv_k[0]+joy_inv_k[1])+r3*math.cos(joy_inv_k[0]+joy_inv_k[1]+joy_inv_k[2]))*scale_factor), 2)
                
                sp = [800, 680] # position of end effector visualization
                pygame.draw.line(screen, (191, 4, 4, 0.8), (sp[0],sp[1]), (scale_factor*10*math.cos(math.radians((target_p[4]-25)*90/65)) + sp[0], -scale_factor*10*math.sin(math.radians((target_p[4]-25)*90/65)) + sp[1]), 2)
                pygame.draw.line(screen, (191, 4, 4, 0.8), (sp[0],sp[1]), (-scale_factor*10*math.cos(math.radians((target_p[4]-25)*90/65)) + sp[0], -scale_factor*10*math.sin(math.radians((target_p[4]-25)*90/65)) + sp[1]), 2)
                pygame.draw.line(screen, (191, 4, 4, 0.8), (scale_factor*10*math.cos(math.radians((target_p[4]-25)*90/65)) + sp[0], -scale_factor*10*math.sin(math.radians((target_p[4]-25)*90/65)) + sp[1]), ((scale_factor*10*math.cos(math.radians((target_p[4]-25)*90/65)) + sp[0], -scale_factor*10*math.sin(math.radians((target_p[4]-25)*90/65)) + (sp[1]-scale_factor*10))), 2)
                pygame.draw.line(screen, (191, 4, 4, 0.8), (-scale_factor*10*math.cos(math.radians((target_p[4]-25)*90/65)) + sp[0], -scale_factor*10*math.sin(math.radians((target_p[4]-25)*90/65)) + sp[1]), ((-scale_factor*10*math.cos(math.radians((target_p[4]-25)*90/65)) + sp[0], -scale_factor*10*math.sin(math.radians((target_p[4]-25)*90/65)) + (sp[1]-scale_factor*10))), 2)
            elif joy_inv_k == "no solution" or joy_inv_k == None:
                if mvmnt == 1:
                    joystick.rumble(0.7, 1, 500)
                    #time.sleep(0.1)
                    #for i in range(2):
                    #axis = joystick.get_axis(0)
                        #if i == 0: #J1 x-axis
                    #if axis > 0.2 or axis < -0.1:
                    target_p[0] += sft[0]#*2
                        #if i == 1: #J1 y-axis
                    #axis = joystick.get_axis(1)
                    #if axis > 0.02 or axis < -0.19:
                    target_p[1] += sft[1]#*2
                    #axis = joystick.get_axis(3)
                    #if axis > 0.02 or axis < -0.19:
                    target_p[3] += sft[2]#*2


            text_print.unindent()
            text_print.tprint(screen, f"Target point: {target_p}")
            text_print.tprint(screen, f"Angles inv_k: {joy_inv_k}")

            buttons = joystick.get_numbuttons()
            text_print.tprint(screen, f"Number of buttons: {buttons}")
            text_print.indent()

            for i in range(buttons):
                button = joystick.get_button(i)
                text_print.tprint(screen, f"Button {i:>2} value: {button}")
            text_print.unindent()

            hats = joystick.get_numhats()
            text_print.tprint(screen, f"Number of hats: {hats}")
            text_print.indent()

            # Hat position. All or nothing for direction, not a float like
            # get_axis(). Position is a tuple of int values (x, y).
            for i in range(hats):
                hat = joystick.get_hat(i)
                text_print.tprint(screen, f"Hat {i} value: {str(hat)}")
            text_print.unindent()

            text_print.unindent()
        
        if mvmnt == 1:
            move_servos(target_p[2], math.degrees(joy_inv_k[0]), math.degrees(joy_inv_k[1]), math.degrees(joy_inv_k[2]), target_p[5], target_p[4])
            

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 30 frames per second.
        clock.tick(30)


if __name__ == "__main__":
    main()
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()