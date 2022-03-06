from math import cos, sin, pi
import time
import socket
import os
import re
from brickpi3 import BrickPi3

BP = BrickPi3()
rightMotor = BP.PORT_A
leftMotor = BP.PORT_D

wheelDiameter = 5
width = 15

stream = os.popen("who am i")
output = stream.read()

UDP_INFO = (re.search("\d+\.\d+\.\d+\.\d+"), 5005)
print(UDP_INFO)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# set robot start position to origin, pointing straight up
x = 0
y = 0
robotAngle = pi / 2
message = "%f,%f" % (x, y)
sock.sendto(message.encode('utf-8'), UDP_INFO)

try:
    BP.offset_motor_encoder(rightMotor, BP.get_motor_encoder(rightMotor))
    BP.offset_motor_encoder(leftMotor, BP.get_motor_encoder(leftMotor))

    while True:
        leftLength = BP.get_motor_encoder(leftMotor)
        rightLength = BP.get_motor_encoder(rightMotor)

        if (leftLength == rightLength):
            x += leftLength*cos(robotAngle)
            y += leftLength*sin(robotAngle)
        else:
            radius = (width * (leftLength + rightLength)) / (2 * (leftLength - rightLength))
            arcAngle = (leftLength - rightLength) / width
            x += radius(sin(robotAngle) - cos(arcAngle) * sin(robotAngle) \
            + sin(arcAngle) * cos(robotAngle))
            y += radius(-cos(robotAngle) + cos(arcAngle) * cos(robotAngle) \
            + sin(arcAngle) * sin(robotAngle))
            
            
        message = "%f,%f" % (x, y)
        sock.sendto(message.encode('utf-8'), UDP_INFO)
        time.sleep(0.05)

    BP.reset_all()
    sock.sendto("stop".encode('utf-8'), UDP_INFO)
except KeyboardInterrupt:
    BP.reset_all()
    sock.sendto("stop".encode('utf-8'), UDP_INFO)
