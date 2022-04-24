import math
from math import pi, cos, sin
import time
import grovepi
from brickpi3 import BrickPi3
import os
import re
import socket

BP = BrickPi3()

rightMotor = BP.PORT_D
leftMotor = BP.PORT_A
rightUltrasonic = 3
leftUltrasonic = 8
frontUltrasonic = BP.PORT_1
legoGyro = BP.PORT_2
wheelDiameter = 56
width = 150

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
    if task == 1:
        instructions = [{'name': 'basicFollow'}]
    elif task == 2:
        instructions = [{'name': 'relativeTurn', 'angle': math.radians(int(input("Input angle: ")))}]
        while True:
            nextAngle = int(input("Input next angle: "))
            if nextAngle == 0:
                break
            else:
                instructions.append({'name': 'relativeTurn', 'angle': math.radians(nextAngle)})
    elif task == 3:
        x = int(input("Enter x: "))
        y = int(input("Enter y: "))
        instructions = [{'name': 'toPoint', 'x': x, 'y': y}]
    elif task == 4:
        while True:
            x = int(input("Input x: "))
            if x == 100:
                break
            else:
                y = int(input("Input y: "))
                instructions.append({'name': 'toPoint', 'x': x, 'y': y})
    elif task == 5:
        instructions.append({'name': 'basicFollow'})
        instructions.append({'name': 'relativeTurn', 'angle': math.pi})
        instructions.append({'name': 'basicFollow'})
    
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
        sock.sendto(message.encode('utf-8'), UDP_INFO)

        if instructions[0]['name'] == 'basicFollow':
            rightDistance = grovepi.digitalRead(rightUltrasonic)
            leftDistance = grovepi.digitalRead(leftUltrasonic)
            frontDistance = BP.get_sensor(frontUltrasonic)
            
            
            
            # handle turning
            if frontDistance > 200 and rightDistance > 50 and leftDistance > 50:
                BP.set_motor_dps(leftMotor, 0)
                BP.set_motor_dps(rightMotor, 0)
                instructions.insert(0, {'name': 'handleFourWay', 'stage': 0})
            elif rightDistance > 30:
                instructions.insert(0, {'name': 'relativeTurn', 'angle': -math.pi / 2})
            elif frontDistance < 20 and frontDistance > 0:
                instructions.insert(0, {'name': 'relativeTurn', 'angle': math.pi / 2})
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
                gyroAngle = BP.get_sensor(legoGyro)
                lastGyroAngle = gyroAngle
                BP.set_motor_dps(leftMotor, 0)
                BP.set_motor_dps(rightMotor, 0)
                Kp = 100
                Ki = 0
                Kd = 30
                lastError = 0
                integral = 0
            relativeAngle = gyroAngle - lastGyroAngle
            error = instructions[0]['angle'] - relativeAngle
            if (error > pi):
                error -= 2 * pi
            elif (error < -pi):
                error += 2 * pi

            if (abs(error) < 0.1):
                instructions.pop(0)
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
            print("Dropoff Code not yet implemented")
            instructions.pop(0)
        
        elif instructions[0]['name'] == 'notify':
            print("notify code not yet impemented")
            instructions.pop(0)
        
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
