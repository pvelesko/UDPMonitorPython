import random
from itertools import count
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

plt.style.use('fivethirtyeight')

t_vals = []
x_vals = []
y_vals = []
z_vals = []

index = count()

fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot([],[], '-')
line2, = ax.plot([],[],'--')
line3, = ax.plot([],[],'--')


# plt.plot(x, y1, label='MagX')
# plt.plot(x, y2, label='MagY')
# plt.plot(x, y3, label='MagZ')
#plt.legend(loc='upper left')
#plt.tight_layout()

def read_data_csv():
    with open("data.csv", "r") as f:
        data = pd.read_csv('data.csv')
        x_dat = data["MagX"]
        y_dat = data["MagY"]
        z_dat = data["MagZ"]
        last_idx = max(0, len(x_vals) - 1)
        #print("x %s y %s z %s" % (x_vals[last_idx], y_vals[last_idx], z_vals[last_idx]))
        return (float(x_dat[last_idx]), float(y_dat[last_idx]), float(z_dat[last_idx]))

ax.set_xlim(0, 500)
ax.set_ylim(-1000, 1000)
def animate(i,):
    x, y, z = read_data_csv()
    #print("t: %s x: %s y: %s z: %s" % (i, x, y, z))
    t_vals.append(i)
    x_vals.append(x)
    y_vals.append(y)
    z_vals.append(z)

    xmin = max(0, i - 500)
    line1.set_xdata(t_vals[:i])
    line2.set_xdata(t_vals[:i])
    line3.set_xdata(t_vals[:i])

    line1.set_ydata(x_vals[:i])
    line2.set_ydata(y_vals[:i])
    line3.set_ydata(z_vals[:i])

    return line1,line2,line3


ani = FuncAnimation(fig, animate, interval=10, blit=True)
# plt.tight_layout()
plt.show()