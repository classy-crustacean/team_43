<<<<<<< HEAD
from math import cos, sin, pi
import time
import socket
import os
import re
from brickpi3 import BrickPi3

BP = BrickPi3()
rightMotor = BP.PORT_D
leftMotor = BP.PORT_A

wheelDiameter = 56
width = 150

stream = os.popen("who am i")
output = stream.read()

UDP_INFO = (re.search("\d+\.\d+\.\d+\.\d+", output).group(0), 5005)
print(UDP_INFO)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# set robot start position to origin, pointing straight up
x = 0
y = 0
robotAngle = pi / 2
leftEncoder = 0
rightEncoder = 0
oldLeftEncoder = 0
oldRightEncoder = 0
rightLength = 0
leftLength = 0
message = "%f,%f" % (x, y)
sock.sendto(message.encode('utf-8'), UDP_INFO)

try:
    BP.offset_motor_encoder(rightMotor, BP.get_motor_encoder(rightMotor))
    BP.offset_motor_encoder(leftMotor, BP.get_motor_encoder(leftMotor))

    while True:
        leftEncoder = -BP.get_motor_encoder(leftMotor)
        rightEncoder = -BP.get_motor_encoder(rightMotor)
        leftLength = pi * wheelDiameter * (leftEncoder - oldLeftEncoder) / 360
        rightLength = pi * wheelDiameter * (rightEncoder - oldRightEncoder) / 360
        oldLeftEncoder = leftEncoder
        oldRightEncoder = rightEncoder

        if (leftLength == rightLength):
            x += leftLength*cos(robotAngle)
            y += leftLength*sin(robotAngle)
        else:
            radius = (width * (leftLength + rightLength)) / (2 * (leftLength - rightLength))
            arcAngle = (leftLength - rightLength) / width
            x += radius * (sin(robotAngle) - cos(arcAngle) * sin(robotAngle) \
            + sin(arcAngle) * cos(robotAngle))
            y += radius * (-cos(robotAngle) + cos(arcAngle) * cos(robotAngle) \
            + sin(arcAngle) * sin(robotAngle))
            robotAngle = robotAngle - arcAngle
            
        message = "%f,%f,%f" % (x, y, robotAngle)
        print(message)
        sock.sendto(message.encode('utf-8'), UDP_INFO)
        time.sleep(0.05)

    BP.reset_all()
    sock.sendto("stop".encode('utf-8'), UDP_INFO)
except KeyboardInterrupt:
    BP.reset_all()
    sock.sendto("stop".encode('utf-8'), UDP_INFO)
=======
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
>>>>>>> 8a05fc8b81484b7a839b0ccd0b81a7230700fbd3
