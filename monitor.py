import socket
import csv
from datetime import datetime
import threading
import numpy as np
import random
from itertools import count
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import time

# UDP_IP = "192.168.175.255" # Phone
UDP_IP = "192.168.1.255" # Home
UDP_PORT = 4210
PACKET_SIZE = 64
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

################# MAIN #################
def receive_data_test():
    print("Checking for incoming data...")
    data, addr = sock.recvfrom(PACKET_SIZE) # buffer size is 1024 bytes
    x, y, z = data.decode("utf-8").split(",")
    t = datetime.timestamp(datetime.now())
    data = {"timestamp": t, "Abs": abs, "MagX": x, "MagY": y, "MagZ": z}
    print(data)


print("Connecting to %s:%s" % (UDP_IP, UDP_PORT))
sock.bind((UDP_IP, UDP_PORT))
receive_data_test()
print("Connection established")
# sock.setblocking(False)

fieldnames = ["timestamp", "Abs", "MagX", "MagY", "MagZ"]
file = open("data.csv", "a")
csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
csv_writer.writeheader()
csv_data = []
# for i in range(0, 100):

# baseline = [];
# for i in range(0, 1000):
#     data, addr = sock.recvfrom(64) # buffer size is 1024 bytes
#     x, y, z = data.decode("utf-8").split(",")
#     t = datetime.timestamp(datetime.now())
#     abs = (float(x)**2 + float(y)**2 + float(z)**2)**0.5
#     baseline.append(abs)
#     abs_avg = sum(baseline)/len(baseline)

mags = [0 for i in range(500)]
t_data = [0 for i in range(500)]
t_diffs = [0 for i in range(500)]
distances = [0 for i in range(500)]




freq = 0
def receive_data():
    t_old = time.perf_counter()
    t_new = time.perf_counter()
    while True:
        data, addr = sock.recvfrom(PACKET_SIZE) # buffer size is 1024 bytes
        x, y, z = data.decode("utf-8").split(",")
        t = datetime.timestamp(datetime.now())
        abs = (float(x)**2 + float(y)**2 + float(z)**2)**0.5
        abs = abs # - abs_avg
        data = {"timestamp": t, "Abs": abs, "MagX": x, "MagY": y, "MagZ": z}
        print(data)
        csv_data.append(data)
        # print("data size: %s" % len(csv_data))
        t_data.append(t)
        mags.append(abs)
        csv_writer.writerow(data)
        t_new = time.perf_counter()
        t_diff = t_new - t_old
        freq = 1/t_diff
        t_diff = round(t_diff * 1000, 3) #  in ms
        t_diffs.append(t_diff)
        # print("freq %s time: %s" % (freq, t_diff))
        t_old = t_new
        # distances.append(calc_displacement(abs))

x = threading.Thread(target=receive_data)
x.start()

plt.style.use('fivethirtyeight')
fig = plt.figure()
ax = fig.subplots(3)
line1, = ax[0].plot([],[], 'b', linewidth=1)
line2, = ax[0].plot([],[], 'r', linewidth=1)
ax[0].set_xlim(0, 500)
ax[0].set_ylim(-1000, 1000)

mag_line, = ax[1].plot([],[], 'r', linewidth=1)
ax[1].set_xlim(0, 500)
ax[1].set_ylim(-1000, 1000)
mag_text = ax[1].text(0, 0, "")

sample_rate_line, = ax[2].plot([],[], 'b', linewidth=1)
sample_fps = ax[2].text(0, 0, freq)

ax[2].set_ylim(0, 105)
ax[2].set_xlim(0, 500)

def animate(frame,):
    t = np.linspace(0, 500, 500)
    end = len(mags)
    start = end - 500
    # rnd = np.random.randint(0, 500, 500)
    rnd = 500 * np.sin(t) + np.random.randint(0, 100, 500)
    mags_plot = np.array(mags[start:end])
    t_diffs_plot = np.array(t_diffs[start:end])

    # distance_plot = np.array(calc_displacement(magnet, sens, mags_plot))


    line1.set_data(t, mags_plot)
    line2.set_data(t, rnd)

    mag_line.set_data(t, mags_plot)
    sample_fps.set_text(freq)

    sample_rate_line.set_data(t, t_diffs_plot)
    idx = min(frame, len(mags)-1)

    end = len(t_diffs)
    start = end - 500

    latest_mag = round(mags_plot[-1], 2)
    mag_text.set_text(latest_mag)
    
    return (line1, line2, sample_rate_line, mag_line, sample_fps, mag_text)


ani = FuncAnimation(fig, animate, interval=1, blit=True, repeat=False)
# ani_samples = FuncAnimation(fig, animate_samples, interval=1, blit=True, repeat=False)
plt.show()
