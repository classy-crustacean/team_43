import math
from math import pi, cos, sin
import time
import grovepi
from brickpi3 import BrickPi3
import os
import re
import socket
import MPU9250
from IR_Functions import *

BP = BrickPi3()

rightMotor = BP.PORT_D
leftMotor = BP.PORT_A
cargoMotor = BP.PORT_B
rightUltrasonic = 3
leftUltrasonic = 8
frontUltrasonic = BP.PORT_1
legoGyro = BP.PORT_2
wheelDiameter = 56
width = 150
myIMU = MPU9250.MPU9250()
IR_setup(grovepi)

integral = 0
lastError = 0

try:
    BP.set_sensor_type(frontUltrasonic, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
    stream = os.popen("who am i")
    output = stream.read()

    UDP_INFO = (re.search("\d+\.\d+\.\d+\.\d+", output).group(0), 5005)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Choose the task to complete
    task = int(input("Enter task number: "))
    instructions = []
    
    x_position = 0
    y_position = 0
    robotAngle = 0
    leftEncoder = 0
    rightEncoder = 0
    oldLeftEncoder = 0
    oldRightEncoder = 0
    rightLength = 0
    leftLength = 0
    
    delay = 0.1

    BP.offset_motor_encoder(rightMotor, BP.get_motor_encoder(rightMotor))
    BP.offset_motor_encoder(leftMotor, BP.get_motor_encoder(leftMotor))

    lastInfo = 0

    while instructions[0]['name'] != 'stop':
        # -----------------
        # Position Tracking
        # -----------------
        leftEncoder = -BP.get_motor_encoder(leftMotor)
        rightEncoder = -BP.get_motor_encoder(rightMotor)
        leftLength = pi * wheelDiameter * (leftEncoder - oldLeftEncoder) / 360
        rightLength = pi * wheelDiameter * (rightEncoder - oldRightEncoder) / 360

        # update last encoder position
        oldLeftEncoder = leftEncoder
        oldRightEncoder = rightEncoder

        # if the wheels turned the same amount, angle didn't change
        if (leftLength == rightLength):
            x_position += leftLength*cos(robotAngle)
            y_position += leftLength*sin(robotAngle)
        else:

            # calculate radius of turn
            radius = (width * (leftLength + rightLength)) \
            / (2 * (leftLength - rightLength))

            # calculate angle of turn
            arcAngle = (leftLength - rightLength) / width

            # calculate new position
            x_position += radius * (sin(robotAngle) - cos(arcAngle) * sin(robotAngle) \
            + sin(arcAngle) * cos(robotAngle))
            y_position += radius * (-cos(robotAngle) + cos(arcAngle) * cos(robotAngle) \
            + sin(arcAngle) * sin(robotAngle))

            # calculate new angle
            robotAngle = (robotAngle - arcAngle) % (2 * pi)
        
        message = "%f,%f,%f" % (x_position, y_position, robotAngle)
        
        gyroAngle = BP.get_sensor(legoGyro)
        magnetValues = myIMU.readMagnet()
        Mag = math.sqrt(magnetValues['x']**2 + magnetValues['y']**2 + magnetValues['z']**2)
        [sensor1_value, sensor2_value] = IR_Read(grovepi)

        if instructions[0]['name'] == 'basicFollow':
            rightDistance = grovepi.digitalRead(rightUltrasonic)
            leftDistance = grovepi.digitalRead(leftUltrasonic)
            frontDistance = BP.get_sensor(frontUltrasonic)
            
            x_comp = None
            y_comp = None
            
            # handle turning
            if frontDistance > 200 and rightDistance > 50 and leftDistance > 50:
                BP.set_motor_dps(leftMotor, 0)
                BP.set_motor_dps(rightMotor, 0)
                instructions.insert(0, {'name': 'handleFourWay', 'stage': 0})
            elif rightDistance > 30:
                instructions.insert(0, {'name': 'relativeTurn', 'angle': -math.pi / 2})
            elif frontDistance < 20 and frontDistance > 0:
                instructions.insert(0, {'name': 'relativeTurn', 'angle': math.pi / 2})
                
            elif Mag >= 150 and magnetValues['x'] > 0:
                theta = math.atan(magnetValues['x']/magnetValues['y'])
                x_comp = 16*math.sin(theta) # This is the value for how far in front of the GEARS the magnetic source is
                y_comp = 16*math.cos(theta) # This is the value for how far side to side the magnetic source is
                if magnetValues['y'] < 0:
                    y_comp *= -1
                instructions.insert(0, {'name': 'relativeTurn', 'angle': math.pi / 2})
                message += ",%s,%f,%f" % ('magnet', x_comp, y_comp)
                
            elif sensor1_value+sensor2_value >= 130:
                instructions.insert(0, {'name': 'relativeTurn', 'angle': math.pi / 2})
                message += ",%s,%f" % ('infrared', 15)
            else:
                error = leftDistance - rightDistance

                if lastInfo != 'basicFollow':
                    Kp = 10
                    Ki = 0
                    Kd = 5
                    baseSpeed = 180
                    lastError = error
                    integral = 0
                
                integral = integral + error * delay
                derivative = (error - lastError) / delay

                modifier = Kp * error + Ki * integral + Kd * derivative

                BP.set_motor_dps(leftMotor, -baseSpeed + modifier)
                BP.set_motor_dps(rightMotor, -baseSpeed - modifier)

                lastError = error
        elif instructions[0]['name'] == 'relativeTurn':
            if lastInfo != 'relativeTurn':
                firstGyroAngle = None
                BP.set_motor_dps(leftMotor, 0)
                BP.set_motor_dps(rightMotor, 0)
                Kp = 100
                Ki = 0
                Kd = 30
                lastError = 0
                integral = 0
            if firstGyroAngle == None:
                firstGyroAngle = gyroAngle
            relativeAngle = gyroAngle - firstGyroAngle
            error = instructions[0]['angle'] - relativeAngle
            if (error > pi):
                error -= 2 * pi
            elif (error < -pi):
                error += 2 * pi

            if (abs(error) < 0.1):
                instructions.pop(0)
                firstGyroAngle = None
                BP.set_motor_dps(leftMotor, 0)
                BP.set_motor_dps(rightMotor, 0)
            else:
                integral = integral + error * delay
                derivative = (error - lastError)

                modifier = Kp * error + Ki * integral + Kd * derivative
                BP.set_motor_dps(leftMotor, modifier)
                BP.set_motor_dps(rightMotor, -modifier)

                lastError = error
        
        elif instructions[0]['name'] == 'dropoff':
            if lastInfo != 'dropoff':
                timer = 0
            if timer < 1:
                BP.set_motor_dps(cargoMotor, 90)
            elif timer < 3:
                BP.set_motor_dps(cargoMotor, 0)
                BP.set_motor_dps(rightMotor, -180)
                BP.set_motor_dps(leftMotor, -180)
            else:
                instructions.pop(0)
                BP.set_motor_dps(rightMotor, 0)
                BP.set_motor_dps(leftMotor, 0)
            timer += delay
        
        elif instructions[0]['name'] == 'notify':
            if lastInfo != 'notify':
                timer = 0

            if timer < 3:
                if timer % 1 < 0.5:
                    BP.set_motor_dps(cargoMotor, -180)
                else:
                    BP.set_motor_dps(cargoMotor, 180)
            else:
                instructions.pop(0)

            timer += delay

        
        elif instructions[0]['name'] == 'toPoint':
            goalX = instructions[0]['x'] * 400
            goalY = instructions[0]['y'] * 400
            dist = math.sqrt((goalX - x_position)**2 + (goalY - y_position)**2)
            print(dist)
            if dist < 20:
                instructions.pop(0)
            else:
                goalAngle = math.acos((goalX - x_position) / dist)
                if (goalY - y_position) < 0:
                    goalAngle = 2 * math.pi - goalAngle
                
                goalAngle = goalAngle % (2 * pi)

                error = goalAngle - robotAngle

                if (error > pi):
                    error -= 2 * pi
                elif (error < -pi):
                    error += 2 * pi

                if lastInfo != 'toPoint':
                    Kp = 100
                    Ki = 0
                    Kd = 30
                    baseSpeed = 180
                    lastError = error
                    integral = 0
                
                integral = integral + error * delay
                derivative = (error - lastError) / delay

                modifier = Kp * error + Ki * integral + Kd * derivative

                BP.set_motor_dps(leftMotor, -baseSpeed + modifier)
                BP.set_motor_dps(rightMotor, -baseSpeed - modifier)

                lastError = error
        elif instructions[0]['name'] == 'avoidTurn':
            print("avoid Turn not yet implemented")
            instructions.pop(0)
        elif instructions[0]['name'] == 'handleFourWay':
            stage = instructions[0]['stage']
            instructions[0]['stage'] += 1
            foundCorner = False
            frontUltrasonicDistance = BP.get_sensor(frontUltrasonic)
            
            if stage == 0:
                instructions.insert(0, {'name': 'relativeTurn', 'angle': pi / 4})
            if stage == 1:
                if frontUltrasonicDistance < 50 and frontUltrasonicDistance > 0:
                    foundCorner = True
                instructions.insert(0, {'name': 'relativeTurn', 'angle': -pi / 2})
            if stage == 2:
                if frontUltrasonicDistance < 50 and frontUltrasonicDistance > 0:
                    foundCorner = True
                instructions.insert(0, {'name': 'relativeTurn', 'angle': pi / 4})
            if stage == 3:
                instructions.pop(0)
                if foundCorner:
                    instructions.insert(0, {'name': 'relativeTurn', 'angle': -pi / 2})

        if len(instructions) == 0:
            instructions.append({'name': 'stop'})
        
        lastInfo = instructions[0]['name']
            
        sock.sendto(message.encode('utf-8'), UDP_INFO)
        
        time.sleep(delay)
    
    BP.set_motor_dps(leftMotor, 0)
    BP.set_motor_dps(rightMotor, 0)
    time.sleep(1)
    BP.reset_all()
    sock.sendto("stop".encode('utf-8'), UDP_INFO)

except KeyboardInterrupt:
    print("Terminated Early")
    BP.reset_all()
    sock.sendto("stop".encode('utf-8'), UDP_INFO)
