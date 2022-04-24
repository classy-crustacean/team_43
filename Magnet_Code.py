import brickpi3, grovepi, math, time, MPU9250
#If the magnitude of the magnetic field is greater than 150, we mark
#it on the map and then move away from that course.
BP = brickpi3.BrickPi3()

myIMU = MPU9250.MPU9250()


# This should be continually running as the robot moves forward
Mag = 0
while True:
    ans = input('Y/N: ')
    if ans == 'Y':
        values = myIMU.readMagnet()
        mag = (values['x'],values['y'],values['z'])
        Mag = math.sqrt(values['x']**2+values['y']**2+values['z']**2)
        print(Mag)
        print(mag)
    else:
        break
    ans = None
    time.sleep(0.1)