import pygame
from pygame import *
clock = time.Clock()
import pygame, serial, time

#firmata stuff

import pyfirmata
from pyfirmata import Arduino, util
waited = False
motor_board = Arduino("/dev/ttyACM0")
#servo_board = Arduino("/dev/ttyUSB0")
#run 'ls /dev/tty*' in terminal to get what port it's connected to

iterator1 = util.Iterator(motor_board)
#iterator2 = util.Iterator(servo_board)
iterator1.start()
#iterator2.start()

#setup
step1 = motor_board.get_pin("d:2:o")
dir1 = motor_board.get_pin("d:5:o")

step2 = motor_board.get_pin("d:3:o")
dir2 = motor_board.get_pin("d:6:o")

step3 = motor_board.get_pin("d:4:o")
dirZ = motor_board.get_pin("d:7:o")

enPin = motor_board.get_pin("d:8:o")

#servo board
#serZ = servo_board.get_pin("d:9:o")

#writing
enPin.write(0)
dir1.write(1)
dir2.write(0)
dirZ.write(1)

ccw = 0
cw = 1

pygame.init()
 
# Set the width and height of the screen [width,height]
#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print

speed = 150

def move_motors(motor1, motor2, xy, speed):
    print(motor1, motor2, xy, speed)
    if motor1 == -1: #if motor 1 doesn't need to be moved
        dir2.write(motor2)
        for i in range(round(xy*speed)): 
            step2.write(1)
            time.sleep(0.001)
            step2.write(0)
    elif motor2 == -1: #if motor 2 doesn't need to be moved
        dir1.write(motor1)
        for i in range(round(xy*speed)): 
            step1.write(1)
            time.sleep(0.001)
            step1.write(0)
    else: #diagonal movement for both
        dir1.write(motor1)
        dir2.write(motor2)
        for i in range(round(xy*speed)): 
            step1.write(1)
            step2.write(1)
            time.sleep(0.001)
            step1.write(0)
            step2.write(0)

#serZ.write(1)
while done==False:
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

    x_coor = joystick.get_axis(0)
    y_coor = joystick.get_axis(1)
    c_coor = joystick.get_axis(3)
    z_coor = joystick.get_axis(4)

    print("x: ", x_coor, "\ty: ", y_coor,"\tc_coor: ",c_coor,"\tz_coor: ",z_coor)

    abs_x = abs(x_coor)
    abs_y = abs(y_coor)
    abs_c = abs(c_coor)

    #move_motors(dir1, dir2, speed)

    #more sensitive to 0
    y_coor = 0 if -0.1<y_coor<0.1 else y_coor
    x_coor = 0 if -0.1<x_coor<0.1 else x_coor
    
    xy = (abs_x**2 + abs_y**2)**0.5
    
    #up
    if y_coor < 0 and x_coor == 0:
        move_motors(ccw, cw, xy, speed)
    #down
    elif y_coor > 0 and x_coor == 0:
        move_motors(cw, ccw, xy, speed)
    #left
    elif y_coor == 0 and x_coor < 0:
        move_motors(ccw, ccw, xy, speed)
    #right
    elif y_coor == 0 and x_coor > 0:
        move_motors(cw, cw, xy, speed)
    #up left
    elif y_coor < 0 and x_coor < 0:
        move_motors(ccw, -1, xy, speed)
    #down right
    elif y_coor > 0 and x_coor > 0:
        move_motors(cw, -1, xy, speed)
    #down left
    elif y_coor > 0 and x_coor < 0:
        move_motors(-1, ccw, xy, speed)
    #up right
    elif y_coor < 0 and x_coor > 0:
        move_motors(-1, cw, xy, speed)

    #print("motor 1: {:>6.3f}".format(move_m1))
    #print("motor 2: {:>6.3f}".format(-move_m2))
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
