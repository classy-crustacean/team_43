import numpy as np
import time
import socket

UDP_INFO = ("10.1.1.10", 5005)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


for i in range(10):
    y = np.random.random()
    message = "%d,%d" % (i, y)
    sock.sendto(message.encode('utf-8'), UDP_INFO)
    time.sleep(0.05)

sock.sendto("stop".encode('utf-8'), UDP_INFO)
