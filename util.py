## IMPORT DATA
from numpy import genfromtxt

def load_data(filename):
    my_data = genfromtxt(filename, delimiter=',')
    my_data = my_data[1:]
    b_abs = [reading[4] for reading in my_data]
    time = [reading[0] for reading in my_data]
    return time, b_abs

def load_data_sensor(filename):
    my_data = genfromtxt(filename, delimiter=',')
    my_data = my_data[1:]
    b_abs = [reading[1] for reading in my_data]
    time = [reading[0] for reading in my_data]
    return time, b_abs