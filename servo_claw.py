import pygame
from pygame import *

from pyfirmata import Arduino, SERVO
from time import sleep

waited = False

pygame.init()
 
#Loop until the user clicks the close button.
done = False

# Initialize the joysticks
pygame.joystick.init()
    

port = '/dev/ttyUSB0'
pin_c = 9
pin_z = 10
board = Arduino(port)

board.digital[pin_c].mode = SERVO
board.digital[pin_z].mode = SERVO

angle_c = 0
angle_z = 0

def rotateServo(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.01)
    
claw = True #True = open , False = Closed

while done == False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    #x_coor = joystick.get_axis(0)
    #y_coor = joystick.get_axis(1)
    c_coor = joystick.get_axis(3)
    z_coor = joystick.get_axis(4)
    
    abs_c = abs(c_coor)
    abs_z = abs(z_coor)

    #checks absolute value to allow a 'threshold'    
    if abs_c < 0.2:
        rotateServo(pin_c, 90)
    elif c_coor < -0.2 and angle_c > -85: #ccw
        for i in range(0,2):
            rotateServo(pin_c, 180)
            angle_c -= 6
    elif c_coor > 0.2 and angle_c < 85: #cw
        for i in range(0,2):
            rotateServo(pin_c, 0)
            angle_c += 6
    else:
        rotateServo(pin_c, 90)

    print("c:",c_coor, angle_c, "// z:",z_coor, angle_z)
    if abs_z < 0.2:
        rotateServo(pin_z, 94)
        sleep(0.01)
    elif z_coor < -0.2 and angle_z > -5: #ccw
        for i in range(0,2):
            rotateServo(pin_z, 180)
            angle_z -= 1
    elif z_coor > 0.2 and angle_z < 5: #cw
        for i in range(0,2):
            rotateServo(pin_z, 0)
            angle_z += 1
    else:
        rotateServo(pin_z, 94)

pygame.quit()
