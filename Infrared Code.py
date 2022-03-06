import grovepi, brickpi3, math, time, MPU9250

BP = brickpi3.brickpi3()

infrared_sensor = 8

thres = input('Give me the threshold for the IR sensor: ')

grovepi.pinMode(infrared_sensor, thres)

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