import time
import socket
import random

UDP_INFO = ("10.1.1.102", 5005)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


for i in range(10):
    y = random.randrange(10)
    message = "%d,%d" % (i, y)
    sock.sendto(message.encode('utf-8'), UDP_INFO)
    time.sleep(0.05)

sock.sendto("stop".encode('utf-8'), UDP_INFO)
