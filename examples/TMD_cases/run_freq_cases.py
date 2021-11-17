import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


data = np.loadtxt('results.txt', delimiter=',')

mass = data[:, 0]
diameters = data[:, 1:4]
thickness = data[:, 4:7]
tower_damage = data[:, 7]
freqs = data[:, 8]

indices = np.argsort(freqs)

for items in zip(freqs[indices], diameters[indices], thickness[indices]):
    print(items)
exit()