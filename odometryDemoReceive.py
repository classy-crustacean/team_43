import matplotlib.pyplot as plt
import numpy as np
import socket
import time

UDP_INFO =  ("10.1.1.102", 5005)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(UDP_INFO)

plt.axis([0, 10, 0, 1])

while True:
    data, addr = sock.recvfrom(1024)
    data = data.decode('utf-8')
    if data == "stop":
        break
    else:
        data = data.split(',')
        plt.scatter(data[0], data[1])
        plt.pause(0.01)

plt.show()
