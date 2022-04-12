# ENG1P13 - The Grappler (P4)
Uses the [Pyfirmata](https://pypi.org/project/pyFirmata/) and [Pygame Joystick class](pygame.org/docs/ref/joystick.html).

Hosted on a Raspberry Pi with two Arduinos and one PS4 controller connected. One Arduino has two motors mounted on a CNC shield, and another has two continuous servos connected.

Motors control the gantry (using [COREXY](corexy.com/theory.html)), and the servos are mounted on a claw mechanism. One opens/closes the claw, and another controls the z-axis.

Initial code was built and referenced off of [Wahid Bawa's RoboticsFSE](https://github.com/WahidBawa/RoboticsFSE).

##### note - for every arduino board that you want to use pyfirmata on, you first have to write the StandardPyfirmata program onto it using the Arduino IDE (file > examples > firmata > standardfirmata) so that the Arduino can actually read and run whatever python code you're writing to it

### okay let me flex the project first


## motor_xy_gantry.py
* Initialize Arduino boards using Pyfirmata
* For semi-smooth movement, you'd want to loop them (the longer the for loop range, the better)
* the ranges in move_motors() change according to how much the joystick axis is
* main while loop constantly checks for joystick action (using our beloved pygame)
* I just specified which joystick axes referenced which direction, but you can access every. last. button. status and information using the pygame joystick class - read the documentation!
* hardcoded all the possible directions (there's only 8) because COREXY is very *unique* but it's super cool
* that's it. motors are fairly straightforward to work with.

#### The only things I would look out for when working with motors:
* code isn't working? literally, try turning it on and off. that includes unplugging the power, restarting the pi, double checking your code
* unplug your motors when you're not using them. seriously, they need to cool down.
* make sure you're plugging them into the motor controllers on the CNC shield consistently, otherwise the directions may be flipped. mark 'em or something
* don't electrocute yourself
* have fun!

## servo_claw.py
I have emotional trauma debugging this with my teammate. Servos suck when I can't find enough documentation on them. Thank goodness for youtube tutorials though.

* same initializing gimmick with the motors - initialize Arduino boards for pyfirmata
* make sure to set the pins to servo, so you can write "degrees" to them (you'll learn why they're "like this" later)
* rotateServo() just makes it more compact, but you're really just writing an angle
* 0 = counter clockwise (ccw), 90 = stay where you are, 180 = clockwise (cw) - THIS IS IMPORTANT
* same while loop thing that works with the pygame module, and the joystick class to check for activity and referencing data to control aforementioned servos
* c -> claw (open/close) - was set up using a gear and pinion mechanism to convert rotational motion into translational motion
* z -> z-axis (up-down) - used another rotational->linear motion mechanism
* yeah you thought that it'd be straightforward right? just input the degree you want, and it'll go to that degree, right?
* WRONG
#### welcome to the niches of servos with pyfirmata
* since servos are constantly in a state of writing information, you can't really tell it to 'stop' as you could with using detach() in arduino
* so to work around this, once you're at the position you want to stop at, you have to say, okay, turn to 90deg (aka DON'T MOVE)
* but if you did want to move it, regardless of whether you're inputting 0 or 40 or anything under 90, you'll ALWAYS do a full 270deg rotation (if you allow it to carry through the entire motion). maybe if you overwrite it with another command, it'll stop prior to turning a full 270, but you never know. does it make sense? NO. is it annoying? YES.
* oh yeah, you want to throw any servo rotation into a for loop with whatever range you'd like.

Yeah that's about the end of that. my team didn't bother working through the niches of servos with pyfirmata because it was legitimately a pain, and we had about 20 minutes before our presentation.

Check out [my website](https://yuxiqin.ca), I guess. Hope my pain was able to help you out just a tiny bit.
