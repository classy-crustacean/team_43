import grovepi, brickpi3, math, time, MPU9250
from IR_Functions import *

BP = brickpi3.BrickPi3()
IR_setup(grovepi)
# If both add up to 100 or more, leave this direction/path
while True:
    ans = input('Y/N: ')
    if ans == 'Y':
        [sensor1_value, sensor2_value]=IR_Read(grovepi)
        print ("One = " + str(sensor1_value) + "\tTwo = " + str(sensor2_value))
        time.sleep(.1)
    else:
        break
#thres = input('Give me the threshold for the IR sensor: ')

'''
while True:
    try:
        if grovepi.digitalRead(infrared_sensor) == 0:
            # Run position code
            break
        else:
            pass
        time.sleep(0.5)
    
    except IOError:
        print("Error")
'''