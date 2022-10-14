import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []
z_vals = []

index = count()


def animate(i):
    data = pd.read_csv('data.csv')
    x = data['timestamp']
    y1 = data['MagX']
    y2 = data['MagY']
    y3 = data['MagZ']

    plt.cla()

    plt.plot(x, y1, label='MagX')
    plt.plot(x, y2, label='MagY')
    plt.plot(x, y3, label='MagZ')

    plt.legend(loc='upper left')
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=10)

plt.tight_layout()
plt.show()