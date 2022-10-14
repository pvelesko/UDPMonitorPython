import socket
import csv
from datetime import datetime

UDP_IP = "192.168.1.255"
UDP_PORT = 4210

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

fieldnames = ["timestamp", "MagX", "MagY", "MagZ"]
file = open("data.csv", "a")
csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
csv_writer.writeheader()
# for i in range(0, 100):
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    x, y, z = data.decode("utf-8").split(",")
    t = datetime.timestamp(datetime.now())
    data = {"timestamp": t, "MagX": x, "MagY": y, "MagZ": z}
    #print("received message: %s" % data
    csv_writer.writerow(data)