import matplotlib.pyplot as plt
import numpy as np
import socket
import time
import os
import re

ip_address = None

stream = os.popen('ipconfig')
sections = re.split('\n\n', stream.read())
sec = None
for i in range(2, len(sections), 2):
    if (sections[i].__contains__("scouting.pi")):
        ip_address = re.search("\d+\.\d+\.\d+\.\d+", re.search("IPv4 Address.*\n", sections[i]).group(0)).group(0)


UDP_INFO =  (ip_address, 5005)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(UDP_INFO)

plt.axis([0, 10, 0, 10])

while True:
    data, addr = sock.recvfrom(1024)
    data = data.decode('utf-8')
    print(data)
    if data == "stop":
        break
    else:
        data = data.split(',')
        plt.scatter(float(data[0]), int(data[1]))
        plt.pause(0.01)

plt.show()
