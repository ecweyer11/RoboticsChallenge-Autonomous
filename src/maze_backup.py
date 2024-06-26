#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
left_drive_smart = Motor(Ports.PORT7, 3.0, True)
right_drive_smart = Motor(Ports.PORT12, 3.0, False)

drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 200)
distance_front_1 = Distance(Ports.PORT9)
distance_right = Distance(Ports.PORT11)
distance_left = Distance(Ports.PORT8)
distance_front_2 = Distance(Ports.PORT10)



# Make random actually random
def setRandomSeedUsingAccel():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    urandom.seed(int(xaxis + yaxis + zaxis))
    
# Set random seed 
setRandomSeedUsingAccel()

vexcode_initial_drivetrain_calibration_completed = False
def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    global vexcode_initial_drivetrain_calibration_completed
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    brain_inertial.calibrate()
    while brain_inertial.is_calibrating():
        sleep(25, MSEC)
    vexcode_initial_drivetrain_calibration_completed = True
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      Self Driving Robot 
# 	Author:       Eli Weyer
# 	Created:      3/5/24
# 	Description:  Source code for a Self Driving Robot. 
#                 Created for New Visions Engineering 
#                 Robotics Challenge.
#   Updated:      3/7/24
# 
# ------------------------------------------

# Import Random Library
import random
import math

# Calibrate Robot CPU
brain.screen.set_font(FontType.MONO15)
brain.screen.print("Calibrating")
brain.screen.next_row()
brain.screen.print("Remain Still")
brain.screen.next_row()
brain.screen.print("Approx. Time:")
brain.screen.next_row()
brain.screen.print("5 Seconds")
brain_inertial.calibrate()
brain_inertial.set_heading(0.0, DEGREES)
brain_inertial.set_rotation(0.0, DEGREES)
currentHeading = brain_inertial.heading()
wait(5, SECONDS)

brain.screen.clear_screen()
brain.screen.set_cursor(1, 1)
brain.play_sound(SoundType.TADA)
brain.screen.print("Complete!")
wait(2, SECONDS)

brain.screen.clear_screen()
brain.screen.set_cursor(1, 1)

# Initialize and Calibrate Robot Sensors and Devices
drivetrain.set_stopping(HOLD)
drivetrain.set_heading(0.0, DEGREES)
drivetrain.set_rotation(0.0, DEGREES)

brain.play_note(4, 5, 500)
brain.screen.print("Devices:")
brain.screen.next_row()
brain.screen.print(drivetrain)
brain.screen.next_row()
brain.screen.print(distance_front_1)
brain.screen.next_row()
brain.screen.print(distance_front_2)
brain.screen.next_row()
brain.screen.print(distance_left)
brain.screen.next_row()
brain.screen.print(distance_right)
wait(3, SECONDS)

brain.screen.clear_screen()
brain.screen.set_cursor(1, 1)

# Maze Challenge Logic

DISTANCE_THRESHOLD = 200 # millimeters

def adjustRotation(goalRotation):
    currentRotation = brain_inertial.rotation()

    if currentRotation != goalRotation:
        brain.screen.print("Adjusting Heading")
        print("Adjusting Heading")
        drivetrain.stop()
        drivetrain.turn_to_rotation(goalRotation, DEGREES, wait=True)
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)

def handleSingleObstacle(isObstacleLeft):
    if isObstacleLeft:
        handleObstacle("left")
    else:
        handleObstacle("right")

def handleObstacle(obstacleDirection):

    if obstacleDirection == "front":
        brain.screen.print("Object Front!")
        print("Object Front!")
        drivetrain.stop()

        SENSOR_SEPARATION = 83 # Millimeters
        DELTA_THRESHOLD = 5 # Degrees
        deltaFrontDistance = distance_front_2.object_distance(MM) - distance_front_1.object_distance(MM)

        if abs(deltaFrontDistance) < DELTA_THRESHOLD:
            sideSensorCheck()
        else:
            turnRadius = round(math.degrees(math.atan(SENSOR_SEPARATION/deltaFrontDistance)))
            turn(turnRadius)

    elif obstacleDirection == "left":
        brain.screen.print("Turning Right!")
        print("Turning Right!")
        drivetrain.turn_for(RIGHT, currentHeading + 90, DEGREES, wait=True)

    elif obstacleDirection == "right":
        brain.screen.print("Turning Left!")
        print("Turning Left!")
        drivetrain.turn_for(LEFT, currentHeading + 90, DEGREES, wait=True)

    elif obstacleDirection == "both":
        print("Intersection!")
        drivetrain.stop()
        brain.screen.print("Turning Left!")
        print("Turning Left!")
        drivetrain.turn_for(LEFT, currentHeading + 90, DEGREES, wait=True)

    else:
        print("Dead End!")
        drivetrain.stop()
        brain.screen.print("Turning Left!")
        print("Turning Left!")
        drivetrain.turn_for(LEFT, currentHeading + 90, DEGREES, wait=True)

def turn(turnRadius):
    drivetrain.set_rotation(0, DEGREES)
    brain_inertial.set_rotation(0, DEGREES)

    if turnRadius < 0:
        print("turning LEFT for ", abs(turnRadius), " degrees")
        drivetrain.turn_to_rotation(turnRadius, DEGREES, wait=True)
        wait(1, SECONDS)
        adjustRotation(turnRadius)
    else:
        print("turning RIGHT for ", turnRadius, " degrees")
        drivetrain.turn_to_rotation(turnRadius, DEGREES, wait=True)
        wait(1, SECONDS)
        adjustRotation(turnRadius)

def sideSensorCheck():

    distanceLeft = distance_left.object_distance(MM)
    distanceRight = distance_right.object_distance(MM)

    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

    if distanceLeft < DISTANCE_THRESHOLD and distanceRight < DISTANCE_THRESHOLD:
        handleObstacle("both")
    
    elif distanceLeft < DISTANCE_THRESHOLD or distanceRight < DISTANCE_THRESHOLD:
        handleSingleObstacle(distanceLeft < DISTANCE_THRESHOLD)
        
    else:
        handleObstacle("all")

def mazeChallenge():
    try:
        while True:
            distanceFront1 = distance_front_1.object_distance(MM)
            distanceFront2 = distance_front_2.object_distance(MM)
        
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)

            while distanceFront1 < DISTANCE_THRESHOLD or distanceFront2 < DISTANCE_THRESHOLD:
                handleObstacle("front")
                break

            brain.screen.print("Driving...")
            print("Driving...")
            drivetrain.set_drive_velocity(35, PERCENT)
            drivetrain.set_turn_velocity(10, PERCENT)
            drivetrain.drive(FORWARD)

    except Exception as e:
        brain.screen.print("Error!")
        brain.screen.next_row()
        brain.screen.print(e)
        print("Error! ", e)
        
mazeChallenge()
