import brickpi3, grovepi, math, time, MPU9250

BP = brickpi3.BrickPi3()

myIMU = MPU9250.MPU9250()


# This should be continually running as the robot moves forward
Mag = 0
while True:
    Mag = math.sqrt(myIMU.readMagnet()['x']**2+myIMU.readMagnet()['y']**2+myIMU.readMagnet()['z']**2)
    if Mag > 40:
        break
    time.sleep(0.1)