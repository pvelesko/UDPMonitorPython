import numpy as np
from scipy.optimize import root

# calculate B-field return uT
def calc_b_field(magnet, sensor, distance):
    distance = abs(distance)
    # disp = np.linspace((0,0,0), (0, 0, distance), 100)
    magnet.position=(0, 0, 0)
    magnet.move((0, 0, distance))

    B = sensor.getB(magnet)
    B_mag = [np.linalg.norm(B_coord) for B_coord in B]
    return B_mag[-1] * 1000

def calc_b_field_vec(magnet, sensor, distances):
    b_mag_vector = []
    for distance in distances:
        magnet.position=(0, 0, 0)
        magnet.move((0, 0, distance))

        B = sensor.getB(magnet)
        B_mag = [np.linalg.norm(B_coord) for B_coord in B]
        b_mag_vector.append(B_mag[-1] * 1000)
    return b_mag_vector

b_field_precomputed = calc_b_field_vec(magnet, sens, np.linspace(1, 500, 500))

# caculate distance given uT return mm
@np.vectorize
def calc_displacement(magnet, sensor, MagReading):
    def f(distance):
        return calc_b_field(magnet, sensor, distance) - MagReading
    r = root(f, 0, tol=0.1)
    return abs(r.x[0])

@np.vectorize
def calc_displacement(magnet, sensor, MagReading):
    def f(distance):
        return calc_b_field(magnet, sensor, distance) - MagReading
    r = root(f, 0, tol=0.1)
    return abs(r.x[0])

def calc_signal_stats(signal):
    noise_std_dev = np.std(signal)
    noise_min = np.min(signal)
    noise_max = np.max(signal)
    noise_delta = noise_max - noise_min
    avg = np.average(signal)
    print("Min: ", noise_min)
    print("Max: ", noise_max)
    print("Average: ", avg)
    print("Standard Deviation: ", noise_std_dev)
    print("Delta:", noise_delta)
    print("\n")